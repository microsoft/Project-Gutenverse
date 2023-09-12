import {
    Mesh,
    MeshBuilder,
    NodeMaterial,
    Scene,
    ShadowGenerator,
    StandardMaterial,
    Texture,
    TextureBlock,
    Tools,
    Vector3,
} from "@babylonjs/core";

import paperBg from "../../assets/paperbg.jpg";
import backgroundGround from "../../assets/backgroundGround.png";

export type CharacterData = {
    name: string;
    imageUrl: string;
    position: Vector3;
    rotation: Vector3;
};

export class Character {
    public sprite?: Mesh;
    constructor(
        public data: CharacterData,
        public scene: Scene,
        public shadowGenerator: ShadowGenerator
    ) {}

    async build() {
        const sprite1 = MeshBuilder.CreatePlane(
            "sprite1",
            { width: 5, height: 7.2 },
            this.scene
        );
        const material1 = await NodeMaterial.ParseFromSnippetAsync("#4HTEHD#5");
        const inputTex = new Texture(this.data.imageUrl, this.scene);
        const texBlock = material1.getBlockByName("Texture") as TextureBlock;
        texBlock.texture = inputTex;
        material1.backFaceCulling = false;
        sprite1.material = material1;
        material1.build(true);

        sprite1.position.z = 2;
        this.shadowGenerator.addShadowCaster(sprite1);

        const shadowFloor = MeshBuilder.CreateGround(
            "floor",
            { width: 5, height: 5 },
            this.scene
        );
        const floorMat = new StandardMaterial("floorMat", this.scene);
        floorMat.emissiveTexture = new Texture(paperBg, this.scene);
        floorMat.opacityTexture = new Texture(backgroundGround, this.scene);
        shadowFloor.material = floorMat;
        shadowFloor.receiveShadows = true;
        shadowFloor.position.set(0, -2.65, 0);
        shadowFloor.parent = sprite1;

        this.sprite = sprite1;

        this.sprite.position = this.data.position;
        this.sprite.rotation = this.data.rotation;
    }
}
