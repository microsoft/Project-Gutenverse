import { SceneArgs } from "../createScene";
import { Player } from "../lib/player";
import { BasicStorybookScene } from "./basicStorybookScene";

export class StoryPlayer {
    public currentSceneIndex = 0;
    public player: Player;
    public currSceneElements?: BasicStorybookScene;

    constructor(public storyContent: any, public sceneArgs: SceneArgs) {
        this.player = new Player(this.sceneArgs.scene, [], () => this.previousScene(), () => this.nextScene());
    }

    public async playScene() {
        this.player.currentTextIndex = 0;
        this.player.textToPlay = this.storyContent.scenes[this.currentSceneIndex].speech;

        const sceneElements = new BasicStorybookScene();
        this.currSceneElements = sceneElements;
        sceneElements.characters = this.storyContent.scenes[this.currentSceneIndex].characters;
        sceneElements.speech = this.storyContent.scenes[this.currentSceneIndex].speech;
        sceneElements.envUrl = this.storyContent.scenes[this.currentSceneIndex].environment;

        await sceneElements.populate(this.sceneArgs);
    }

    public disposeScene() {
        if (this.currSceneElements) {
            this.currSceneElements.dispose(this.sceneArgs);
        }
    }

    public nextScene() {
        if (this.currentSceneIndex < this.storyContent.scenes.length) {
            this.disposeScene();
            this.currentSceneIndex++;
            this.playScene();
        }
    }

    public previousScene() {
        if (this.currentSceneIndex > 0) {
            this.disposeScene();
            this.currentSceneIndex--;
            this.playScene();
        }
    }
}