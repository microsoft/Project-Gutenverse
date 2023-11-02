// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

import { Sound } from "@babylonjs/core";
import { SceneArgs } from "../createScene";
import { Player } from "../lib/player";
import { BasicStorybookScene } from "./basicStorybookScene";

export class StoryPlayer {
    public currentSceneIndex = 0;
    public player: Player;
    public currSceneElements?: BasicStorybookScene;
    public currSceneSound?: Sound;
    public currSceneBackgroundMusic?: Sound;

    constructor(public storyContent: any, public sceneArgs: SceneArgs) {
        this.player = new Player(this.sceneArgs.scene, [], () => this.previousScene(), () => this.nextScene());
    }

    public async playScene() {
        console.log('in play scene, curr index is', this.currentSceneIndex, 'max length', this.storyContent.scenes.length);
        this.player.currentTextIndex = 0;
        this.player.textToPlay = this.storyContent.scenes[this.currentSceneIndex]["speech"] || [];
        this.player.updateText();

        if (this.storyContent.scenes[this.currentSceneIndex].music) {
            console.log('loading sound from url', "http://localhost:5000" + this.storyContent.scenes[this.currentSceneIndex].music);
            this.currSceneBackgroundMusic = new Sound("backgroundMusic", "http://localhost:5000" + this.storyContent.scenes[this.currentSceneIndex].music, this.sceneArgs.scene, () => {
                this.currSceneBackgroundMusic!.play();
                this.currSceneBackgroundMusic?.setVolume(.1);
                this.player.updateBackgroundMusic(this.currSceneBackgroundMusic!);
            }, {loop: true});
        }

        if (this.storyContent.scenes[this.currentSceneIndex]["speech"][0].tts) {
            console.log('loading text to speech from url', "http://localhost:5000" + this.storyContent.scenes[this.currentSceneIndex]["speech"][0].tts);
            this.currSceneSound = new Sound("backgroundMusic", "http://localhost:5000" + this.storyContent.scenes[this.currentSceneIndex]["speech"][0].tts, this.sceneArgs.scene, () => {
                this.currSceneSound!.play();
                this.currSceneSound!.loop = false;
                this.player.updateSound(this.currSceneSound!);
            }, {loop: true});
        }
        const sceneElements = new BasicStorybookScene();
        this.currSceneElements = sceneElements;
        sceneElements.characters = this.storyContent.scenes[this.currentSceneIndex].characters;
        sceneElements.speech = this.storyContent.scenes[this.currentSceneIndex].speech;
        sceneElements.envUrl = this.storyContent.scenes[this.currentSceneIndex].environment;

        await sceneElements.populate(this.sceneArgs);
    }

    public disposeScene() {
        if (this.currSceneBackgroundMusic) {
            this.currSceneBackgroundMusic.dispose();
        }

        if (this.currSceneSound) {
            this.currSceneSound.dispose();
        }
        if (this.currSceneElements) {
            this.currSceneElements.dispose(this.sceneArgs);
        }
    }

    public nextScene() {
        console.log('in next scene, curr index is', this.currentSceneIndex, 'max', this.storyContent.scenes.length);
        if (this.currentSceneIndex < this.storyContent.scenes.length - 1) {
            console.log('dispose prev scene and play nexst');
            this.disposeScene();
            this.currentSceneIndex++;
            this.playScene();
        }
    }

    public previousScene() {
        console.log('in previous scene, curr index is', this.currentSceneIndex);
        if (this.currentSceneIndex > 0) {
            this.disposeScene();
            this.currentSceneIndex--;
            this.playScene();
        }
    }
}