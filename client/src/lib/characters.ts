// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

import {
    ActionManager,
    Camera,
    Color3,
    ExecuteCodeAction,
    HighlightLayer,
    Mesh,
    MeshBuilder,
    NodeMaterial,
    PlaySoundAction,
    Quaternion,
    Scene,
    ShadowDepthWrapper,
    ShadowGenerator,
    Sound,
    StandardMaterial,
    Texture,
    TextureBlock,
    Tools,
    Vector3,
} from "@babylonjs/core";

const SIZE_MULT = 10;

export type CharacterData = {
    name: string;
    imageUrl: string;
    soundEffect: string;
    distanceFromCamera: number;
    angularDistanceFromCamera: number;
    width: number;
    height: number;
    distanceFromGround: number;
};

import soundUrl from "../../public/assets/audio/671175__tgerginov__magic.wav";

export class Character {
    public sprite?: Mesh;
    public material?: StandardMaterial;
    public tex?: Texture;
    constructor(
        public data: CharacterData,
        public scene: Scene,
        public shadowGenerator: ShadowGenerator
    ) {}

    dispose() {
        this.sprite?.dispose();
        this.material?.dispose();
        this.tex?.dispose();
    }

    async build(camera: Camera) {
        if (this.data.imageUrl) {
            const sprite1 = MeshBuilder.CreatePlane(
                this.data.name,
                { width: this.data.width*SIZE_MULT, height: this.data.height*SIZE_MULT },
                this.scene
            );
            const hightlight = new HighlightLayer("hl" + this.data.name, this.scene);
            const sound = new Sound("plim", "http://localhost:5000" + this.data.soundEffect);
            sound.setVolume(.5);
            sprite1.actionManager = new ActionManager(this.scene);
            sprite1.actionManager.registerAction(
                new PlaySoundAction(
                    ActionManager.OnPickTrigger,
                    sound
                ));
            sprite1.actionManager.registerAction(
                new ExecuteCodeAction(
                    ActionManager.OnPointerOverTrigger,
                    () => {
                        hightlight.addMesh(sprite1, Color3.Green());
                    }
                )
            );
            sprite1.actionManager.registerAction(
                new ExecuteCodeAction(
                    ActionManager.OnPointerOutTrigger,
                    () => {
                        hightlight.removeMesh(sprite1);
                    }
                )
            );
 
            this.material = new StandardMaterial("CharacterMat_" + this.data.name, this.scene);
            const inputTex = new Texture(
                "http://localhost:5000" + this.data.imageUrl,
                this.scene
            );
        
            inputTex.hasAlpha = true;
            this.material.emissiveTexture = inputTex;
            this.material.diffuseTexture = inputTex;
            this.material.emissiveColor = Color3.White();
            this.material.ambientColor = Color3.White();
            this.material.backFaceCulling = false;
     
           
            sprite1.material = this.material;
   

            this.shadowGenerator.addShadowCaster(sprite1);

            sprite1.renderingGroupId = 1;

            this.sprite = sprite1;

            // calculate position to place sprite
            const cameraDirection = camera.getDirection(new Vector3(0, 0, 1));
            cameraDirection.y = 0;

            const rotatedCameraDirection =
                cameraDirection.applyRotationQuaternion(
                    Quaternion.FromEulerAngles(
                        0,
                        Tools.ToRadians(this.data.angularDistanceFromCamera),
                        0
                    )
                );
            this.sprite.position = new Vector3(
                camera.position.x,
                0,
                camera.position.z
            ).add(rotatedCameraDirection.scale(this.data.distanceFromCamera));

            this.sprite.position.y +=
                this.data.distanceFromGround + this.data.height / 2;
        }
    }
}
