import { BasicStorybookScene } from "./basicStorybookScene";

import princessPenguinUrl from "../../assets/characters/princesspenguin.png";
import dragonUrl from "../../assets/characters/dragon.png";
import environmentUrl from "../../assets/environment/blockade_env.png";
import soundUrl from "../../assets/audio/Kevin_MacLeod_The_Forest_and_the_Trees.mp3";

export class PrincessAndDragonScene extends BasicStorybookScene {
    constructor() {
        super();
        this.characters = [
            {name: "Princess", imageUrl: princessPenguinUrl, distanceFromCamera: 60, angularDistanceFromCamera: -7, width: 5, height: 7.2, distanceFromGround: 0},
            {name: "Dragon", imageUrl: dragonUrl, distanceFromCamera: 60, angularDistanceFromCamera: 7, width: 10, height: 14.2, distanceFromGround: 0},
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
        this.soundUrl = soundUrl;
    }
}

export default new PrincessAndDragonScene();
