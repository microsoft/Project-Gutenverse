import {Nullable, Scene, Sound} from "@babylonjs/core";
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
    public playSoundButton?: Nullable<Control>;
    public stopSoundButton?: Nullable<Control>;
    public openSettingsButton?: Control;
    public settingsModal?: Control;
    public closeSettingsButton?: Control;
    public backgroundMusicSlider?: ImageBasedSlider;
    public storyNarrationSlider?: ImageBasedSlider;
    public speechGui?: AdvancedDynamicTexture;
    public isSoundPlaying = true;

    constructor(public scene: Scene, public textToPlay: TextFormat[], public previousSceneCallback?: Callback, public nextSceneCallback?: Callback, public sound?: Sound) {
        AdvancedDynamicTexture.ParseFromSnippetAsync("#CEVEMZ#8").then((gui) => {
            this.speechGui = gui;
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
            console.log('previous scene button', this.previousSceneButton);
            if (!previousSceneCallback) {
                this.previousSceneButton.isVisible = false;
            } else {
                console.log('set previous scene callback');
                this.previousSceneButton.onPointerUpObservable.add(() => {
                    console.log('clicked on previous scene button');
                    this.previousSceneButton!.isEnabled = false;
                    this.previousSceneCallback!();
                    this.previousSceneButton!.isEnabled = true;
                });
            }
            this.nextSceneButton = gui.getControlByName("NextScene")!;
            console.log('next scene button', this.nextSceneButton);
            if (!nextSceneCallback) {
                this.nextSceneButton.isVisible = false;
            } else {
                console.log("set next scene callback");
                this.nextSceneButton.onPointerUpObservable.add(() => {
                    console.log('clicked on next scene button');
                    this.nextSceneButton!.isEnabled = false;
                    this.nextSceneCallback!();
                    this.nextSceneButton!.isEnabled = true;
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

    updateSound = (sound: Sound) => {
        this.sound = sound;
        this.playSoundButton = this.speechGui?.getControlByName("PlaySound");
        this.stopSoundButton = this.speechGui?.getControlByName("StopSound");
        if (!this.playSoundButton || !this.stopSoundButton) {
            return;
        }
        if (!this.sound) {
            this.playSoundButton.isVisible = false;
            this.stopSoundButton.isVisible = false;
        } else {
            console.log('set up play and stop sound button');
            this.playSoundButton.onPointerUpObservable.add(() => {
                if (!this.isSoundPlaying) {
                    console.log('clicked on play sound button');
                    this.sound!.play();
                    this.isSoundPlaying = true;
                }
            });
            this.stopSoundButton.onPointerUpObservable.add(() => {
                console.log('clicked on stop sound button');
                this.sound!.stop();
                this.isSoundPlaying = false;
            });
        }
    }

    updateText() {
        if (this.text) {
            const character = this.textToPlay[this.currentTextIndex].character;
            const text = this.textToPlay[this.currentTextIndex].text;
            this.text.text = `${character}: ${text}`;
        }
    }
}