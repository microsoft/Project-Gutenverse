import { Tools } from "@babylonjs/core";
import { Vector3 } from "@babylonjs/core/Maths/math.vector";


import "@babylonjs/core/Loading/loadingScreen";
import "@babylonjs/loaders/glTF";
import "@babylonjs/core/Materials/standardMaterial";
import "@babylonjs/core/Materials/Textures/Loaders/envTextureLoader";



import { BasicStorybookScene } from "./basicStorybookScene";

import princessPenguinUrl from "../../assets/characters/princesspenguin.png";
import dragonUrl from "../../assets/characters/dragon.png";
import environmentUrl from "../../assets/environment/blockade_env.png";

export class PrincessAndDragonScene extends BasicStorybookScene {
    constructor() {
        super();
        this.characters = [
            {name: "Princess", imageUrl: princessPenguinUrl, position: new Vector3(-8, -5.21, -0.95), rotation: new Vector3(0, Tools.ToRadians(-63.59), 0)},
            {name: "Dragon", imageUrl: dragonUrl, position: new Vector3(-14.78, -3.28, 3.63), rotation: new Vector3(0, Tools.ToRadians(298), 0)},
        ];
        this.speech = [
            {character: "Princess", text: "Hello, I am the princess!"},
            {character: "Dragon", text: "Hello, I am the dragon!"},
            {character: "Princess", text: "Are you a friend or a foe?"},
            {character: "Dragon", text: "I am a friend!"},
            {character: "Princess", text: "Do you want to play a game?"},
            {character: "Dragon", text: "Yes!"},
            {character: "Princess", text: "Let's go to my castle!"}
        ];
        this.envUrl = environmentUrl;
        this.nextScene = "princessAndDragon2";
    }
}

export default new PrincessAndDragonScene();
