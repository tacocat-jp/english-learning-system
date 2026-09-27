from src.CompositionRoot import dependency_injection

if __name__ == "__main__":
    # 依存注入
    main_window = dependency_injection()
    
    # メイン
    main_window.create_frame()
    main_window.loop()
    