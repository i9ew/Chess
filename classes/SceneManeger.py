class SceneManeger:
    def __init__(self, scenes):
        self.scenes = scenes
        self.activeScene = None

    def process_scene(self, screen, events, events_p):
        self.activeScene.input_processing(events, events_p)
        self.activeScene.update()
        self.activeScene.render(screen)
        if self.activeScene.next:
            self.activeScene = self.activeScene.next
            self.activeScene = self.activeScene()

    def goto_scene(self, scenename):
        self.activeScene = self.scenes[scenename]()
        self.activeScene.scene_manager = self
