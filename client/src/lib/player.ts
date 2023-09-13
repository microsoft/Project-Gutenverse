import {Scene, Sound} from "@babylonjs/core";
import {AdvancedDynamicTexture, Control, TextBlock, ImageBasedSlider} from "@babylonjs/gui";
import { Callback } from "../createScene";

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
    public openSettingsButton?: Control;
    public settingsModal?: Control;
    public closeSettingsButton?: Control;
    public backgroundMusicSlider?: ImageBasedSlider;
    public storyNarrationSlider?: ImageBasedSlider;

    constructor(public scene: Scene, public textToPlay: TextFormat[], public previousSceneCallback?: Callback, public nextSceneCallback?: Callback, public sound?: Sound) {
        AdvancedDynamicTexture.ParseFromSnippetAsync("#CEVEMZ#12").then((gui) => {
            gui.layer!.applyPostProcess = false;
            this.openSettingsButton = gui.getControlByName("OpenSettings")!;

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
            console.log('previous scene button', this.previousSceneButton);
            if (!previousSceneCallback) {
                this.previousSceneButton.isVisible = false;
            } else {
                this.previousSceneButton.onPointerUpObservable.add(() => {
                    console.log('clicked on previous scene button');
                    this.previousSceneCallback!();
                });
            }
            this.nextSceneButton = gui.getControlByName("NextScene")!;
            console.log('next scene button', this.nextSceneButton);
            if (!nextSceneCallback) {
                this.nextSceneButton.isVisible = false;
            } else {
                this.nextSceneButton.onPointerUpObservable.add(() => {
                    console.log('clicked on next scene button');
                    this.nextSceneCallback!();
                });
            }
            this.updateText();

            // Single spot for play/pause button that changes based on play/pause status
            this.playSoundButton = gui.getControlByName("Play")!;
            this.stopSoundButton = gui.getControlByName("Pause")!;

            // adding the false in if statement for testing purposes
            if (!this.sound && false) {
                this.playSoundButton!.isVisible = false;
                this.stopSoundButton!.isVisible = false;
            } else {
                // assuming autoplay sound when scene starts
                this.playSoundButton.isVisible = false;

                this.stopSoundButton.onPointerUpObservable.add(() => {
                    console.log('clicked on stop sound button');
                    this.stopSoundButton!.isVisible = false;
                    this.playSoundButton!.isVisible = true;
                    //this.sound!.stop();
                });

                this.playSoundButton.onPointerUpObservable.add(() => {
                    console.log('clicked on play sound button');
                    this.playSoundButton!.isVisible = false;
                    this.stopSoundButton!.isVisible = true;
                    //this.sound!.play();
                });
            }

            // this.playSoundButton = gui.getControlByName("PlaySound")!;
            // this.stopSoundButton = gui.getControlByName("StopSound")!;
            // if (!this.sound) {
            //     this.playSoundButton.isVisible = false;
            //     this.stopSoundButton.isVisible = false;
            // } else {
            //     this.playSoundButton.onPointerUpObservable.add(() => {
            //         console.log('clicked on play sound button');
            //         this.sound!.play();
            //     });
            //     this.stopSoundButton.onPointerUpObservable.add(() => {
            //         console.log('clicked on stop sound button');
            //         this.sound!.stop();
            //     });
            // }
        });

        AdvancedDynamicTexture.ParseFromSnippetAsync("#JF6IFS#8").then((gui) => {
            gui.layer!.applyPostProcess = false;
            
            this.settingsModal = gui.getControlByName("SettingsModal")!;
            this.settingsModal.isVisible = false;

            // Open Settings Modal
            this.openSettingsButton?.onPointerUpObservable.add(() => {
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