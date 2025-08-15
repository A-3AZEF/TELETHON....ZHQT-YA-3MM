import os

def load_sessions():
    if not os.path.exists('sessions'):
        os.makedirs('sessions')
    
    sessions = [f.split('.')[0] for f in os.listdir('sessions') if f.endswith('.session')]
    return sessions