from src.Adapter.MainWindow.ImageSwicherViewModel import ImageSwicherViewModel
from src.Adapter.UpdateController.UpdateController import UpdateController
from src.Adapter.LLMPort.GrammarCorrectedLLMPort import GrammarCorrectedLLMPort
from src.Adapter.LLMPort.GrammarExplanationLLMPort import GrammarExplanationLLMPort
from src.Adapter.LLMPort.MeaningCorrectedLLMPort import MeaningCorrectedLLMPort
from src.Adapter.LLMPort.MeaningExplanationLLMPort import MeaningExplanationLLMPort
from src.Adapter.LLMPort.PronunciationLLMPort import PronunciationLLMPort
from src.Adapter.LLMPort.AlternativeAnswerLLMPort import AlternativeAnswerLLMPort
from src.Infrastructure.MainWindow.MainWindow import MainWindow
from src.Infrastructure.Player.SoundDevicePlayer import SoundDevicePlayer
from src.Infrastructure.Recorder.SoundDeviceRecorder import SoundDeviceRecorder
from src.Infrastructure.Transcriber.FasterWisperTranscriber import FasterWisperTranscriber
from src.Infrastructure.LLMClient.GemmaClient import GemmaClient
from src.Infrastructure.TextToSpeech.Piper import Piper
from src.UseCase.EnglishLearningSystem import EnglishLearningSystem

def dependency_injection():
    
    main_window = MainWindow(ImageSwicherViewModel())
    
    gateways = {
        'player'                  : SoundDevicePlayer(),
        'recorder'                : SoundDeviceRecorder(),
        'speech_transcriber'      : FasterWisperTranscriber(),
        'grammar_corrected'       : GrammarCorrectedLLMPort(GemmaClient()),
        'grammar_explanation'     : GrammarExplanationLLMPort(GemmaClient()),
        'meaning_corrected'       : MeaningCorrectedLLMPort(GemmaClient()),
        'meaning_explanation'     : MeaningExplanationLLMPort(GemmaClient()),
        'pronunciation'           : PronunciationLLMPort(GemmaClient()),
        'alternative_answer'      : AlternativeAnswerLLMPort(GemmaClient()),
        'text_to_speech'          : Piper(),
        'update_controller'       : UpdateController(main_window),
        'text_updater'            : main_window,
    }
    
    english_learning_system = EnglishLearningSystem(gateways)
    
    main_window.dependency_injection(english_learning_system)
    
    return main_window
