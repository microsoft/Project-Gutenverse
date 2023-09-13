import {Scene, Sound} from "@babylonjs/core";
import {AdvancedDynamicTexture, Control, TextBlock} from "@babylonjs/gui";

export type TextFormat = {character: string, text: string};

export class Player {
    public speechBubble?: Control;
    public forwardButton?: Control;
    public backButton?: Control;
    public text?: TextBlock;
    public previousSceneButton?: Control;
    public nextSceneButton?: Control;
    public currentTextIndex = 0;
    public playSoundButton?: Control;
    public stopSoundButton?: Control;

    constructor(public scene: Scene, public textToPlay: TextFormat[], public previousScene?: string, public nextScene?: string, public sound?: Sound) {
        AdvancedDynamicTexture.ParseFromSnippetAsync("#CEVEMZ#5").then((gui) => {
            gui.layer!.applyPostProcess = false;
            this.speechBubble = gui.getControlByName("SpeechBlock")!;
            this.forwardButton = gui.getControlByName("Foward")!;
            this.forwardButton.onPointerUpObservable.add(() => {
                console.log('clicked on forward button');
                if (this.currentTextIndex < this.textToPlay.length - 1) {
                    this.currentTextIndex++;
                }
                this.updateText();
            });
            this.backButton = gui.getControlByName("Back")!;
            this.backButton.onPointerUpObservable.add(() => {
                console.log('clicked on back button');
                if (this.currentTextIndex > 0) {
                    this.currentTextIndex--;
                }
                this.updateText();
            });
            this.text = gui.getControlByName("Text")! as TextBlock;
            this.previousSceneButton = gui.getControlByName("PreviousScene")!;
            if (!previousScene) {
                this.previousSceneButton.isVisible = false;
            } else {
                this.previousSceneButton.onPointerUpObservable.add(() => {
                    console.log('clicked on previous scene button');
                    this.replaceScene(previousScene);
                });
            }
            this.nextSceneButton = gui.getControlByName("NextScene")!;
            if (!nextScene) {
                this.nextSceneButton.isVisible = false;
            } else {
                this.nextSceneButton.onPointerUpObservable.add(() => {
                    console.log('clicked on next scene button');
                    this.replaceScene(nextScene);
                });
            }
            this.updateText();

            this.playSoundButton = gui.getControlByName("PlaySound")!;
            this.stopSoundButton = gui.getControlByName("StopSound")!;
            if (!this.sound) {
                this.playSoundButton.isVisible = false;
                this.stopSoundButton.isVisible = false;
            } else {
                this.playSoundButton.onPointerUpObservable.add(() => {
                    console.log('clicked on play sound button');
                    this.sound!.play();
                });
                this.stopSoundButton.onPointerUpObservable.add(() => {
                    console.log('clicked on stop sound button');
                    this.sound!.stop();
                });
            }
        });
    }

    replaceScene(sceneName: string) {
        const currentLoc = window.location.href.split("?")[0];
        window.location.href = `${currentLoc}?scene=${sceneName}`;
    }

    updateText() {
        if (this.text) {
            const character = this.textToPlay[this.currentTextIndex].character;
            const text = this.textToPlay[this.currentTextIndex].text;
            this.text.text = `${character}: ${text}`;
        }
    }
}