import {Scene} from "@babylonjs/core";
import {AdvancedDynamicTexture, Control, TextBlock, ImageBasedSlider} from "@babylonjs/gui";

export type TextFormat = {character: string, text: string};

export class Player {
    public speechBubble?: Control;
    public forwardButton?: Control;
    public backButton?: Control;
    public text?: TextBlock;
    public previousSceneButton?: Control;
    public nextSceneButton?: Control;
    public currentTextIndex = 0;

    public openSettingsButton?: Control;
    public settingsModal?: Control;
    public closeSettingsButton?: Control;
    public backgroundMusicSlider?: ImageBasedSlider;
    public storyNarrationSlider?: ImageBasedSlider;

    constructor(public scene: Scene, public textToPlay: TextFormat[], public previousScene?: string, public nextScene?: string) {
        AdvancedDynamicTexture.ParseFromSnippetAsync("#CEVEMZ#2").then((gui) => {
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
        });

        AdvancedDynamicTexture.ParseFromSnippetAsync("#JF6IFS#7").then((gui) => {
            this.settingsModal = gui.getControlByName("SettingsModal")!;
            this.settingsModal.isVisible = false;

            // Open Settings Modal
            this.openSettingsButton = gui.getControlByName("OpenSettings")!;
            this.openSettingsButton.onPointerUpObservable.add(() => {
                console.log('clicked on open settings');
                if (this.settingsModal) {
                    this.settingsModal.isVisible = true;
                }
            });

            // Close Settings Modal
            this.closeSettingsButton = gui.getControlByName("CloseSettings")!;
            this.closeSettingsButton.onPointerUpObservable.add(() => {
                console.log('clicked on close settings');
                if (this.settingsModal) {
                    this.settingsModal.isVisible = false;
                }
            });

            // Adjust Background Music Volume Slider
            this.backgroundMusicSlider = <ImageBasedSlider>gui.getControlByName("BackgroundMusicVolume")!;
            this.backgroundMusicSlider.onValueChangedObservable.add(function(value: any) {
                console.log('Background Music Volume: ', value);
            });

            // Adjust Story Narration Volume Slider
            this.storyNarrationSlider = <ImageBasedSlider>gui.getControlByName("StoryNarrationVolume")!;
            this.storyNarrationSlider?.onValueChangedObservable.add(function(value: any) {
                console.log('Story Narration Volume: ', value);
            });

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