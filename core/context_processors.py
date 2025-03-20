from django.conf import settings
import os

def environment_settings(request):
    """Add environment variables to the template context."""
    env = os.environ.get('DJANGO_ENV', 'development')
    
    # Allow previewing production fonts via query parameter
    if request.GET.get('preview_env'):
        env = request.GET.get('preview_env')
    
    # Map environments to font families
    env_fonts = {
        'development': "'Comic Sans MS', 'Comic Sans', cursive",
        'staging': "'Georgia', serif",
        'production': "'IM Fell English', serif",  # Ensure this is correctly set for production
        # Add other environments as needed
    }
    
    # If environment is not in the mapping, use a default
    font_family = env_fonts.get(env, env_fonts['production'])
    
    # You can also change other styling based on environment
    env_colors = {
        'development': "#f8d7da",  # Light red
        'staging': "#fff3cd",      # Light yellow
        'production': "transparent"  # No special color
    }
    
    return {
        'ENVIRONMENT': env,
        'ENV_FONT_FAMILY': font_family,
        'ENV_COLOR': env_colors.get(env, env_colors['production']),
    } 