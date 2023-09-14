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

    constructor(public scene: Scene, public textToPlay: TextFormat[], public previousSceneCallback?: Callback, public nextSceneCallback?: Callback, public sound?: Sound, public backgroundMusic?: Sound) {
        AdvancedDynamicTexture.ParseFromSnippetAsync("#CEVEMZ#12").then((gui) => {
            this.speechGui = gui;
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

    updateBackgroundMusic = (music: Sound) => {
        this.backgroundMusic = music;
    }

    updateSound = (sound: Sound) => {
        this.sound = sound;
        if (!this.speechGui) {
            return;
        }
        // Single spot for play/pause button that changes based on play/pause status
        this.playSoundButton = this.speechGui.getControlByName("Play");
        this.stopSoundButton = this.speechGui.getControlByName("Pause");
        if (!this.playSoundButton || !this.stopSoundButton) {
            return;
        }
        // adding the false in if statement for testing purposes
        if (!this.sound) {
            this.playSoundButton!.isVisible = false;
            this.stopSoundButton!.isVisible = false;
        } else {
            // assuming autoplay sound when scene starts
            this.playSoundButton.isVisible = false;

            this.stopSoundButton.onPointerUpObservable.add(() => {
                console.log('clicked on stop sound button');
                this.stopSoundButton!.isVisible = false;
                this.playSoundButton!.isVisible = true;
                this.sound?.stop();
                this.backgroundMusic?.stop();
            });

            this.playSoundButton.onPointerUpObservable.add(() => {
                console.log('clicked on play sound button');
                this.playSoundButton!.isVisible = false;
                this.stopSoundButton!.isVisible = true;
                this.sound?.play();
                this.backgroundMusic?.play();
            });
        }
    }

    updateText() {
        if (this.text && this.textToPlay) {
            const character = this.textToPlay[this.currentTextIndex].character;
            const text = this.textToPlay[this.currentTextIndex].text;
            this.text.text = `${character}: ${text}`;
        }
    }
}