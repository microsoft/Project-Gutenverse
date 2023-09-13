import { BasicStorybookScene } from "./basicStorybookScene";

import princessPenguinUrl from "../../assets/characters/princesspenguin.png";
import dragonUrl from "../../assets/characters/dragon.png";
import envUrl from "../../assets/environment/castle_background.png";

export class PrincessAndDragonScene2 extends BasicStorybookScene {
    constructor() {
        super();
        this.characters = [
            {name: "Princess", imageUrl: princessPenguinUrl, distanceFromCamera: 40, angularDistanceFromCamera: -15, width: 5, height: 7.2, distanceFromGround: 0},
            {name: "Dragon", imageUrl: dragonUrl, distanceFromCamera: 40, angularDistanceFromCamera: 15, width: 10, height: 14.2, distanceFromGround: 0},
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