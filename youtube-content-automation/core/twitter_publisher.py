"""
Twitter/X Publisher - Publica vídeos e conteúdo no X (Twitter).

Suporta:
- Upload de vídeos (até 140 segundos para conta padrão)
- Upload de imagens
- Criação de tweets com mídia
- Criação de threads
"""

import os
import time
import logging
from typing import Optional, List, Dict
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TwitterPublisher:
    """Publica conteúdo no Twitter/X."""
    
    # Limites do Twitter
    MAX_VIDEO_DURATION = 140  # segundos (conta padrão)
    MAX_VIDEO_SIZE = 512 * 1024 * 1024  # 512 MB
    MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB
    MAX_TWEET_LENGTH = 280
    
    def __init__(self):
        """Inicializa o publisher com credenciais do ambiente."""
        self.bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
        self.consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
        self.consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
        self.access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        self.access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
        
        self._client = None
        self._api_v1 = None
    
    @property
    def is_configured(self) -> bool:
        """Verifica se todas as credenciais estão configuradas."""
        return all([
            self.consumer_key,
            self.consumer_secret,
            self.access_token,
            self.access_token_secret,
        ])
    
    def _get_client(self):
        """Obtém cliente tweepy para API v2."""
        if self._client is None:
            try:
                import tweepy
                self._client = tweepy.Client(
                    bearer_token=self.bearer_token,
                    consumer_key=self.consumer_key,
                    consumer_secret=self.consumer_secret,
                    access_token=self.access_token,
                    access_token_secret=self.access_token_secret,
                    wait_on_rate_limit=True,
                )
            except ImportError:
                raise ImportError("Instale tweepy: pip install tweepy")
        return self._client
    
    def _get_api_v1(self):
        """Obtém API v1.1 para upload de mídia."""
        if self._api_v1 is None:
            try:
                import tweepy
                auth = tweepy.OAuth1UserHandler(
                    self.consumer_key,
                    self.consumer_secret,
                    self.access_token,
                    self.access_token_secret,
                )
                self._api_v1 = tweepy.API(auth, wait_on_rate_limit=True)
            except ImportError:
                raise ImportError("Instale tweepy: pip install tweepy")
        return self._api_v1
    
    def upload_video(self, video_path: str) -> Optional[str]:
        """
        Faz upload de um vídeo para o Twitter.
        
        Args:
            video_path: Caminho do arquivo de vídeo
            
        Returns:
            media_id do vídeo ou None se falhar
        """
        if not self.is_configured:
            logger.error("Credenciais do Twitter não configuradas")
            return None
        
        video_path = Path(video_path)
        if not video_path.exists():
            logger.error(f"Vídeo não encontrado: {video_path}")
            return None
        
        file_size = video_path.stat().st_size
        if file_size > self.MAX_VIDEO_SIZE:
            logger.error(f"Vídeo muito grande: {file_size/1024/1024:.1f}MB (max: 512MB)")
            return None
        
        try:
            api = self._get_api_v1()
            
            logger.info(f"Iniciando upload de vídeo: {video_path.name} ({file_size/1024/1024:.1f}MB)")
            
            # Upload chunked para vídeos grandes
            media = api.media_upload(
                filename=str(video_path),
                media_category="tweet_video",
                chunked=True,
            )
            
            # Aguarda processamento
            logger.info("Aguardando processamento do vídeo...")
            self._wait_for_media_processing(api, media.media_id)
            
            logger.info(f"✅ Vídeo uploaded: media_id={media.media_id}")
            return str(media.media_id)
            
        except Exception as e:
            logger.error(f"Erro no upload do vídeo: {e}")
            return None
    
    def upload_image(self, image_path: str) -> Optional[str]:
        """
        Faz upload de uma imagem para o Twitter.
        
        Args:
            image_path: Caminho do arquivo de imagem
            
        Returns:
            media_id da imagem ou None se falhar
        """
        if not self.is_configured:
            logger.error("Credenciais do Twitter não configuradas")
            return None
        
        image_path = Path(image_path)
        if not image_path.exists():
            logger.error(f"Imagem não encontrada: {image_path}")
            return None
        
        try:
            api = self._get_api_v1()
            media = api.media_upload(filename=str(image_path))
            logger.info(f"✅ Imagem uploaded: media_id={media.media_id}")
            return str(media.media_id)
            
        except Exception as e:
            logger.error(f"Erro no upload da imagem: {e}")
            return None
    
    def _wait_for_media_processing(self, api, media_id: str, max_wait: int = 120):
        """Aguarda o processamento de mídia no Twitter."""
        import tweepy
        
        for i in range(max_wait // 5):
            try:
                status = api.get_media_upload_status(media_id)
                state = status.processing_info.get("state", "succeeded")
                
                if state == "succeeded":
                    return True
                elif state == "failed":
                    error = status.processing_info.get("error", {})
                    logger.error(f"Processamento falhou: {error}")
                    return False
                
                # Ainda processando
                check_after = status.processing_info.get("check_after_secs", 5)
                logger.info(f"  Processando... aguardando {check_after}s")
                time.sleep(check_after)
                
            except tweepy.NotFound:
                # Mídia não encontrada pode significar que já foi processada
                return True
            except Exception as e:
                logger.warning(f"Erro ao verificar status: {e}")
                time.sleep(5)
        
        logger.warning("Timeout aguardando processamento")
        return False
    
    def post_tweet(
        self,
        text: str,
        media_ids: Optional[List[str]] = None,
        reply_to: Optional[str] = None,
    ) -> Optional[Dict]:
        """
        Posta um tweet com texto e mídia opcional.
        
        Args:
            text: Texto do tweet (max 280 caracteres)
            media_ids: Lista de media_ids para anexar
            reply_to: ID do tweet para responder (cria thread)
            
        Returns:
            Dados do tweet criado ou None se falhar
        """
        if not self.is_configured:
            logger.error("Credenciais do Twitter não configuradas")
            return None
        
        # Trunca texto se necessário
        if len(text) > self.MAX_TWEET_LENGTH:
            text = text[:self.MAX_TWEET_LENGTH - 3] + "..."
        
        try:
            client = self._get_client()
            
            kwargs = {"text": text}
            
            if media_ids:
                kwargs["media_ids"] = media_ids
            
            if reply_to:
                kwargs["in_reply_to_tweet_id"] = reply_to
            
            response = client.create_tweet(**kwargs)
            
            tweet_id = response.data["id"]
            logger.info(f"✅ Tweet publicado: https://twitter.com/i/status/{tweet_id}")
            
            return {
                "id": tweet_id,
                "text": text,
                "url": f"https://twitter.com/i/status/{tweet_id}",
            }
            
        except Exception as e:
            logger.error(f"Erro ao publicar tweet: {e}")
            return None
    
    def post_video_with_text(
        self,
        video_path: str,
        text: str,
        hashtags: Optional[List[str]] = None,
    ) -> Optional[Dict]:
        """
        Posta um vídeo com texto e hashtags.
        
        Args:
            video_path: Caminho do vídeo
            text: Texto do tweet
            hashtags: Lista de hashtags (sem #)
            
        Returns:
            Dados do tweet ou None se falhar
        """
        # Adiciona hashtags ao texto
        if hashtags:
            hashtag_str = " ".join(f"#{tag}" for tag in hashtags[:5])  # Max 5 hashtags
            if len(text) + len(hashtag_str) + 1 <= self.MAX_TWEET_LENGTH:
                text = f"{text}\n\n{hashtag_str}"
        
        # Upload do vídeo
        media_id = self.upload_video(video_path)
        if not media_id:
            return None
        
        # Posta tweet
        return self.post_tweet(text, media_ids=[media_id])
    
    def post_psalm(
        self,
        video_path: str,
        psalm_name: str,
        description: Optional[str] = None,
        channel_label: str = "Salmo do Dia",
    ) -> Optional[Dict]:
        """
        Posta um vídeo de salmo ou passagem no Twitter/X.
        
        Args:
            video_path: Caminho do vídeo
            psalm_name: Nome do salmo (ex: "Salmo 23") ou referência (ex: "João 3:16")
            description: Descrição opcional
            channel_label: Rótulo do canal (ex: "Salmo do Dia", "Passagem do Dia")
            
        Returns:
            Dados do tweet ou None se falhar
        """
        text = f"📖 {psalm_name} | {channel_label}"
        
        if description:
            first_line = description.split("\n")[0]
            if len(text) + len(first_line) + 2 <= 200:
                text = f"{text}\n\n{first_line}"
        
        hashtags = ["salmo", "biblia", "fe", "deus", "shorts"]
        return self.post_video_with_text(video_path, text, hashtags)
    
    @staticmethod
    def check_configuration() -> Dict:
        """Verifica a configuração do Twitter."""
        publisher = TwitterPublisher()
        
        status = {
            "configured": publisher.is_configured,
            "credentials": {
                "bearer_token": bool(publisher.bearer_token),
                "consumer_key": bool(publisher.consumer_key),
                "consumer_secret": bool(publisher.consumer_secret),
                "access_token": bool(publisher.access_token),
                "access_token_secret": bool(publisher.access_token_secret),
            },
        }
        
        if publisher.is_configured:
            try:
                client = publisher._get_client()
                me = client.get_me()
                if me.data:
                    status["account"] = {
                        "id": me.data.id,
                        "username": me.data.username,
                        "name": me.data.name,
                    }
                    status["valid"] = True
                else:
                    status["valid"] = False
                    status["error"] = "Não foi possível obter dados da conta"
            except Exception as e:
                status["valid"] = False
                status["error"] = str(e)
        
        return status


# =============================================================================
# FUNÇÕES AUXILIARES
# =============================================================================

def post_salmo_to_twitter(
    video_path: str,
    psalm_name: str,
    description: Optional[str] = None,
) -> Optional[Dict]:
    """
    Função auxiliar para postar salmo no Twitter.
    
    Args:
        video_path: Caminho do vídeo
        psalm_name: Nome do salmo
        description: Descrição opcional
        
    Returns:
        Dados do tweet ou None
    """
    # Carrega variáveis de ambiente se necessário
    from dotenv import load_dotenv
    load_dotenv()
    
    publisher = TwitterPublisher()
    return publisher.post_psalm(video_path, psalm_name, description)


def check_twitter_setup():
    """Verifica e exibe status da configuração do Twitter."""
    from dotenv import load_dotenv
    load_dotenv()
    
    status = TwitterPublisher.check_configuration()
    
    print("\n" + "="*50)
    print("  CONFIGURAÇÃO DO TWITTER/X")
    print("="*50)
    
    print(f"\n📋 Credenciais:")
    for key, configured in status["credentials"].items():
        icon = "✅" if configured else "❌"
        print(f"   {icon} {key}")
    
    if status.get("valid"):
        account = status.get("account", {})
        print(f"\n✅ Conta conectada:")
        print(f"   @{account.get('username')} ({account.get('name')})")
    elif status.get("error"):
        print(f"\n❌ Erro: {status['error']}")
    elif not status["configured"]:
        print("\n⚠️  Configure as credenciais no arquivo .env")
    
    print("="*50 + "\n")
    
    return status


if __name__ == "__main__":
    check_twitter_setup()
