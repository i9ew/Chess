class SceneManeger:
    def __init__(self, scenes):
        self.scenes = scenes
        self.activeScene = scenes["main"]()

    def process_scene(self, screen, events):
        self.activeScene.input_processing(events)
        self.activeScene.update()
        self.activeScene.render(screen)
        if self.activeScene.next:
            self.activeScene = self.activeScene.next
            self.activeScene = self.activeScene()

    def goto_scene(self, scenename):
        self.activeScene = self.scenes[scenename]()
