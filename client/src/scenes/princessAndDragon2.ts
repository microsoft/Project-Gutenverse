import { BasicStorybookScene } from "./basicStorybookScene";

import princessPenguinUrl from "../../assets/characters/princesspenguin.png";
import dragonUrl from "../../assets/characters/dragon.png";
import envUrl from "../../assets/environment/castle_background.png";
import { Tools, Vector3 } from "@babylonjs/core";

export class PrincessAndDragonScene2 extends BasicStorybookScene {
    constructor() {
        super();
        this.characters = [
            {name: "Princess", imageUrl: princessPenguinUrl, position: new Vector3(-8, -5.21, -0.95), rotation: new Vector3(0, Tools.ToRadians(-63.59), 0)},
            {name: "Dragon", imageUrl: dragonUrl, position: new Vector3(-14.78, -3.28, 3.63), rotation: new Vector3(0, Tools.ToRadians(298), 0)},
        ];
        this.speech = [
            {character: "Dragon", text: "Princess, your castle is beautiful!"},
            {character: "Princess", text: "Thank you!"},
            {character: "Dragon", text: "I love the color of the flowers."},
            {character: "Princess", text: "Me too! Do you want to pick flowers?"},
            {character: "Dragon", text: "Yes!"},
        ];
        this.envUrl = envUrl;
        this.previousScene = "princessAndDragon";
    }
}

export default new PrincessAndDragonScene2();