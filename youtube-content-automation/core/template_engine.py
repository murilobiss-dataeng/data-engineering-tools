"""Template engine for video generation."""

import os
import yaml
from typing import Dict, Optional


class TemplateEngine:
    """Load and manage video templates from YAML configuration."""
    
    def __init__(self, templates_dir: str = "config"):
        """Initialize template engine.
        
        Args:
            templates_dir: Directory containing template YAML files
        """
        self.templates_dir = templates_dir
        self.templates_cache = {}
    
    def load_template(self, template_name: str, channel: Optional[str] = None) -> Dict:
        """Load a template by name.
        
        Args:
            template_name: Name of the template
            channel: Optional channel name to load channel-specific template
            
        Returns:
            Template configuration dictionary
        """
        cache_key = f"{channel}_{template_name}" if channel else template_name
        
        if cache_key in self.templates_cache:
            return self.templates_cache[cache_key]
        
        # Try channel-specific template first
        if channel:
            template_path = os.path.join(
                self.templates_dir,
                f"templates_{channel}.yaml"
            )
            if os.path.exists(template_path):
                template = self._load_yaml_template(template_path, template_name)
                if template:
                    self.templates_cache[cache_key] = template
                    return template
        
        # Fall back to default templates
        template_path = os.path.join(self.templates_dir, "templates.yaml")
        if os.path.exists(template_path):
            template = self._load_yaml_template(template_path, template_name)
            if template:
                self.templates_cache[cache_key] = template
                return template
        
        # Return default template if not found
        return self._get_default_template()
    
    def _load_yaml_template(self, file_path: str, template_name: str) -> Optional[Dict]:
        """Load template from YAML file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                templates = yaml.safe_load(f)
                if templates and template_name in templates:
                    return templates[template_name]
        except Exception as e:
            print(f"Error loading template from {file_path}: {e}")
        return None
    
    def _get_default_template(self) -> Dict:
        """Get default template configuration."""
        return {
            'bg_color': (0, 0, 0),
            'text_elements': [
                {
                    'text': '',
                    'position': 'center',
                    'fontsize': 50,
                    'color': 'white',
                    'font': 'Arial-Bold',
                    'bg_color': None,
                    'stroke_color': 'black',
                    'stroke_width': 2
                }
            ],
            'thumbnail_size': (1920, 1080),
            'title_fontsize': 80,
            'title_color': (255, 255, 255),
            'outline_width': 3,
            'outline_color': (0, 0, 0)
        }
    
    def get_shorts_template(self, channel: Optional[str] = None) -> Dict:
        """Get template for shorts videos."""
        template = self.load_template('shorts', channel)
        template['is_shorts'] = True
        return template
    
    def get_long_form_template(self, channel: Optional[str] = None) -> Dict:
        """Get template for long-form videos."""
        template = self.load_template('long_form', channel)
        template['is_shorts'] = False
        return template
    
    def apply_text_to_template(self, template: Dict, text: str, position: str = 'center') -> Dict:
        """Apply text to a template configuration.
        
        Args:
            template: Template configuration
            text: Text to apply
            position: Position of text ('top', 'center', 'bottom')
            
        Returns:
            Updated template configuration
        """
        template = template.copy()
        
        if 'text_elements' not in template or not template['text_elements']:
            template['text_elements'] = [{}]
        
        # Update first text element
        template['text_elements'][0]['text'] = text
        template['text_elements'][0]['position'] = position
        
        return template
