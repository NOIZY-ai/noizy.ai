from enum import Enum, auto
import time

class AvatarState(Enum):
    IDLE = auto()
    LISTEN = auto()
    THINK = auto()
    SPEAK = auto()
    ALERT = auto()
    EXECUTE_CONFIRM = auto()

class GabrielAvatar:
    __slots__ = ['state', 'interrupted']
    
    def __init__(self):
        self.state = AvatarState.IDLE
        self.interrupted = False
        
    def transition(self, new_state: AvatarState):
        print(f"STATE TRANSITION: {self.state.name} -> {new_state.name}")
        self.state = new_state
        
    def listen(self, audio_stream):
        self.transition(AvatarState.LISTEN)
        # Logic to process stream
        
    def speak(self, text: str):
        if self.interrupted:
            print("DUPLEX INTERRUPT: Speech halted.")
            self.transition(AvatarState.LISTEN)
            return
            
        self.transition(AvatarState.SPEAK)
        print(f"SAYING: {text}")
        # Viseme logic would go here
        
    def interrupt(self):
        """External trigger for duplex interruption"""
        self.interrupted = True
        self.transition(AvatarState.LISTEN)

if __name__ == "__main__":
    avatar = GabrielAvatar()
    avatar.speak("Initializing GABRIEL OS...")
    avatar.interrupt()
    avatar.speak("This should not be said.")
