"""Enhanced content generation with better explanations."""

import random
from typing import Dict, List


class EnhancedContentGenerator:
    """Generate high-quality educational content."""
    
    TOPICS_DETAILED = {
        'O que é Inteligência Artificial?': {
            'intro': 'A Inteligência Artificial, ou IA, é uma das tecnologias mais revolucionárias da nossa era.',
            'explanation': 'Ela permite que máquinas aprendam, raciocinem e tomem decisões de forma similar aos humanos. Desde assistentes virtuais até carros autônomos, a IA está transformando nosso dia a dia.',
            'examples': 'Exemplos incluem o ChatGPT, reconhecimento facial, e sistemas de recomendação que você usa em plataformas de streaming.',
            'conclusion': 'A IA não é mais ficção científica - ela já faz parte da nossa realidade e continuará evoluindo.'
        },
        'Como funciona a Blockchain?': {
            'intro': 'Blockchain é uma tecnologia de registro distribuído que revolucionou a forma como armazenamos informações.',
            'explanation': 'Imagine um livro contábil digital que é copiado e distribuído para milhares de computadores. Cada transação é registrada em blocos que são encadeados e protegidos por criptografia.',
            'examples': 'Bitcoin e outras criptomoedas usam blockchain, mas a tecnologia também pode ser aplicada em contratos inteligentes, rastreamento de produtos e muito mais.',
            'conclusion': 'A blockchain oferece transparência, segurança e descentralização, características que estão mudando diversos setores.'
        },
        'O que é Cloud Computing?': {
            'intro': 'Cloud Computing, ou computação em nuvem, é a entrega de serviços de computação pela internet.',
            'explanation': 'Ao invés de ter servidores físicos na sua empresa, você acessa recursos de computação, armazenamento e software através da internet. É como alugar ao invés de comprar.',
            'examples': 'Serviços como Netflix, Gmail, Dropbox e Amazon Web Services são exemplos de cloud computing.',
            'conclusion': 'A nuvem oferece flexibilidade, escalabilidade e economia, permitindo que empresas de todos os tamanhos tenham acesso a tecnologia de ponta.'
        },
        'Como funciona o Machine Learning?': {
            'intro': 'Machine Learning é um subcampo da Inteligência Artificial que permite que sistemas aprendam com dados.',
            'explanation': 'Ao invés de programar cada regra, o sistema analisa grandes quantidades de dados, identifica padrões e aprende a fazer previsões ou tomar decisões automaticamente.',
            'examples': 'Recomendações da Netflix, detecção de spam em emails, e diagnósticos médicos assistidos por IA são exemplos de machine learning em ação.',
            'conclusion': 'Quanto mais dados o sistema processa, melhor ele fica, tornando-se cada vez mais preciso e útil.'
        },
        'O que é DevOps?': {
            'intro': 'DevOps é uma cultura e conjunto de práticas que unem desenvolvimento de software e operações de TI.',
            'explanation': 'O objetivo é reduzir o tempo entre escrever código e colocá-lo em produção, melhorando a colaboração entre equipes e automatizando processos.',
            'examples': 'Ferramentas como Docker, Kubernetes, Jenkins e GitLab CI/CD são comumente usadas em ambientes DevOps.',
            'conclusion': 'DevOps permite entregas mais rápidas, maior qualidade e melhor resposta a mudanças no mercado.'
        },
        'O que são APIs?': {
            'intro': 'API significa Interface de Programação de Aplicações, e é como aplicativos se comunicam entre si.',
            'explanation': 'Imagine uma API como um garçom em um restaurante: você faz um pedido, ele leva para a cozinha e traz sua comida. APIs fazem a mesma coisa, conectando diferentes sistemas.',
            'examples': 'Quando você usa um app de clima, ele usa uma API para buscar dados meteorológicos. Quando faz login com Google em outros sites, está usando a API do Google.',
            'conclusion': 'APIs são a base da internet moderna, permitindo que serviços diferentes trabalhem juntos de forma integrada.'
        },
        'Como funciona a Internet?': {
            'intro': 'A Internet é uma rede global de computadores conectados que permite comunicação e compartilhamento de informações.',
            'explanation': 'Quando você acessa um site, seu computador envia uma solicitação através de roteadores e servidores até chegar ao servidor que hospeda o site. A resposta volta pelo mesmo caminho em milissegundos.',
            'examples': 'Protocolos como TCP/IP, HTTP e DNS são os "idiomas" que os computadores usam para se comunicar na internet.',
            'conclusion': 'A internet funciona através de uma infraestrutura complexa de cabos, satélites e protocolos que tornam possível a comunicação global instantânea.'
        },
        'O que é Big Data?': {
            'intro': 'Big Data refere-se a conjuntos de dados extremamente grandes e complexos que exigem tecnologias especiais para processamento.',
            'explanation': 'São dados que não cabem em sistemas tradicionais e precisam de ferramentas avançadas para análise. Caracterizam-se pelo volume, variedade e velocidade.',
            'examples': 'Redes sociais geram petabytes de dados diariamente. Análise de Big Data ajuda empresas a entender clientes, otimizar operações e tomar decisões estratégicas.',
            'conclusion': 'Big Data transforma informações brutas em insights valiosos, impulsionando inovação e eficiência em diversos setores.'
        },
        'O que é IoT (Internet das Coisas)?': {
            'intro': 'Internet das Coisas, ou IoT, conecta objetos físicos do dia a dia à internet.',
            'explanation': 'Dispositivos como lâmpadas, termostatos, carros e até geladeiras podem se conectar à internet, coletar dados e serem controlados remotamente.',
            'examples': 'Casas inteligentes com Alexa, cidades inteligentes com sensores de trânsito, e wearables como smartwatches são exemplos de IoT.',
            'conclusion': 'IoT está criando um mundo mais conectado e inteligente, onde objetos podem se comunicar e trabalhar juntos para melhorar nossa qualidade de vida.'
        },
        'Como funciona o 5G?': {
            'intro': '5G é a quinta geração de tecnologia de rede móvel, oferecendo velocidades muito superiores ao 4G.',
            'explanation': 'Usa frequências de rádio mais altas e tecnologias avançadas para transmitir dados muito mais rápido, com menor latência e capacidade para conectar muito mais dispositivos simultaneamente.',
            'examples': '5G permite realidade virtual em tempo real, cirurgias remotas, e cidades inteligentes com milhões de sensores conectados.',
            'conclusion': 'O 5G não é apenas internet mais rápida - é a base para tecnologias transformadoras como carros autônomos e telemedicina avançada.'
        }
    }
    
    def __init__(self):
        """Initialize enhanced content generator."""
        pass
    
    def get_random_topic(self) -> str:
        """Get a random topic."""
        topics = list(self.TOPICS_DETAILED.keys())
        return random.choice(topics)
    
    def generate_script(self, topic: str, length: str = 'short') -> str:
        """Generate a high-quality script for a topic.
        
        Args:
            topic: Topic to explain
            length: Script length ('short' or 'long')
            
        Returns:
            Generated script
        """
        topic_data = self.TOPICS_DETAILED.get(topic)
        
        if not topic_data:
            # Fallback for topics not in detailed list
            if length == 'short':
                return f"Hoje vamos explicar: {topic}\n\n{topic} é um conceito importante que vamos desvendar de forma clara e objetiva."
            else:
                return f"Olá! Bem-vindo ao Explicado em Shorts!\n\nHoje vamos explorar: {topic}\n\nEste é um tema fascinante que merece uma explicação detalhada."
        
        if length == 'short':
            script = f"Você já se perguntou: {topic}?\n\n"
            script += f"{topic_data['intro']}\n\n"
            script += f"{topic_data['explanation']}\n\n"
            script += f"{topic_data['examples']}\n\n"
            script += "Se inscreva para mais explicações como esta!"
        else:
            script = f"Olá! Bem-vindo ao Explicado em Shorts!\n\n"
            script += f"Hoje vamos explorar em detalhes: {topic}\n\n"
            script += f"{topic_data['intro']}\n\n"
            script += f"{topic_data['explanation']}\n\n"
            script += f"{topic_data['examples']}\n\n"
            script += f"{topic_data['conclusion']}\n\n"
            script += "Se você gostou, deixe seu like e se inscreva no canal para mais conteúdo educativo!"
        
        return script
