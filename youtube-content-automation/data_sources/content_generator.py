"""Content generation for educational videos."""

import random
from typing import Dict, List


class ContentGenerator:
    """Generate educational content topics and scripts."""
    
    TOPICS = {
        'technology': [
            'O que é Inteligência Artificial?',
            'Como funciona a Blockchain?',
            'O que é Cloud Computing?',
            'Como funciona o Machine Learning?',
            'O que é DevOps?',
            'O que são APIs?',
            'Como funciona a Internet?',
            'O que é Big Data?',
            'O que é IoT (Internet das Coisas)?',
            'Como funciona o 5G?'
        ],
        'science': [
            'O que é a Teoria da Relatividade?',
            'Como funciona a Fotosíntese?',
            'O que são Buracos Negros?',
            'Como funciona o DNA?',
            'O que é a Mecânica Quântica?',
            'Como funciona o Sistema Solar?',
            'O que é a Evolução?',
            'Como funciona o Cérebro?',
            'O que é a Gravidade?',
            'Como funciona a Eletricidade?'
        ],
        'finance': [
            'O que é Inflação?',
            'Como funciona a Bolsa de Valores?',
            'O que são Juros Compostos?',
            'Como funciona o Crédito?',
            'O que é um Fundo de Investimento?',
            'Como funciona o Imposto de Renda?',
            'O que é CDI?',
            'Como funciona a SELIC?',
            'O que é Diversificação?',
            'Como funciona a Aposentadoria?'
        ],
        'general': [
            'O que é Marketing Digital?',
            'Como funciona o Empreendedorismo?',
            'O que é Produtividade?',
            'Como funciona a Comunicação?',
            'O que é Liderança?',
            'Como funciona a Motivação?',
            'O que é Resiliência?',
            'Como funciona a Criatividade?',
            'O que é Inovação?',
            'Como funciona o Networking?'
        ]
    }
    
    def __init__(self):
        """Initialize content generator."""
        pass
    
    def get_random_topic(self, category: str = None) -> str:
        """Get a random topic.
        
        Args:
            category: Topic category (technology, science, finance, general)
            
        Returns:
            Random topic
        """
        if category and category in self.TOPICS:
            topics = self.TOPICS[category]
        else:
            # Get random topic from all categories
            all_topics = []
            for cat_topics in self.TOPICS.values():
                all_topics.extend(cat_topics)
            topics = all_topics
        
        return random.choice(topics)
    
    def generate_script(self, topic: str, length: str = 'short') -> str:
        """Generate a script for a topic.
        
        Args:
            topic: Topic to explain
            length: Script length ('short' or 'long')
            
        Returns:
            Generated script
        """
        # This is a simplified version
        # In production, use GPT or similar for better content generation
        
        if length == 'short':
            script = f"Hoje vamos explicar: {topic}\n\n"
            script += f"{topic} é um conceito importante que muitas pessoas não entendem completamente.\n\n"
            script += "Vamos explicar de forma simples e direta.\n\n"
            script += "Fique até o final para entender tudo sobre este tema!"
        else:
            script = f"Olá! Bem-vindo ao nosso canal.\n\n"
            script += f"Hoje vamos falar sobre: {topic}\n\n"
            script += f"Este é um tema muito interessante e importante.\n\n"
            script += "Vamos começar explicando o básico.\n\n"
            script += "Depois, vamos ver exemplos práticos.\n\n"
            script += "E por fim, vamos entender como isso se aplica no dia a dia.\n\n"
            script += "Não esqueça de se inscrever e deixar seu like!"
        
        return script
    
    def get_all_topics(self) -> List[str]:
        """Get all available topics.
        
        Returns:
            List of all topics
        """
        all_topics = []
        for topics in self.TOPICS.values():
            all_topics.extend(topics)
        return all_topics
