// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

import { Scene, Sound, Texture } from "@babylonjs/core";
import { Character, CharacterData } from "../lib/characters";
import { Player, TextFormat } from "../lib/player";
import { SceneArgs, SceneClass } from "../createScene";


export class BasicStorybookScene implements SceneClass {
    public characters: CharacterData[] = [];
    public speech: TextFormat[] = [];
    public envUrl = "";
    public soundUrl: string | undefined = undefined;
    public sound?: Sound | undefined = undefined;
    public characterObjs: Character[] = [];
    public player?: Player;
    public stageUrl = "";

    populate = async (
        sceneArgs: SceneArgs
    ): Promise<Scene> => {
        const {scene, shadowGenerator} = sceneArgs;
        
        if (this.envUrl) {
            const texture = new Texture("http://localhost:5000" + this.envUrl);
            (sceneArgs.world.material! as any).emissiveTexture = texture;
        }

        if (this.stageUrl) {
            const stageTexture = new Texture("http://localhost:5000" + this.stageUrl);
            (sceneArgs.stage.material! as any).emissiveTexture = stageTexture;
        }

        for (const character of this.characters) {
            const char = new Character(character, scene, shadowGenerator);
            this.characterObjs.push(char);
            await char.build(scene.activeCamera!);
        }

        // if (this.soundUrl) {
        //     this.sound = new Sound("backgroundMusic", this.soundUrl, scene, () => {
        //         this.sound!.play();
        //     });
        // }

        // const gui = new Player(scene, this.speech, undefined, undefined, this.sound);
        // this.player = gui;

        return scene;
    };

    dispose(sceneArgs: SceneArgs) {
        this.characterObjs.forEach((char) => char.dispose());
        if ((sceneArgs.world.material! as any).emissiveTexture) {
            (sceneArgs.world.material! as any).emissiveTexture.dispose();
        }
        if ((sceneArgs.stage.material! as any).emissiveTexture) {
            (sceneArgs.stage.material! as any).emissiveTexture.dispose();
        }
    }
}