import {
    Camera,
    Mesh,
    MeshBuilder,
    NodeMaterial,
    Quaternion,
    Scene,
    ShadowDepthWrapper,
    ShadowGenerator,
    StandardMaterial,
    Texture,
    TextureBlock,
    Tools,
    Vector3,
} from "@babylonjs/core";

export type CharacterData = {
    name: string;
    imageUrl: string;
    distanceFromCamera: number;
    angularDistanceFromCamera: number;
    width: number;
    height: number;
    distanceFromGround: number;
};

export class Character {
    public sprite?: Mesh;
    public material?: NodeMaterial;
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
        const sprite1 = MeshBuilder.CreatePlane(
            this.data.name,
            { width: this.data.width, height: this.data.height },
            this.scene
        );
        const material1 = await NodeMaterial.ParseFromSnippetAsync("#0HR986#1");
        this.material = material1;
        const inputTex = new Texture(this.data.imageUrl, this.scene);
        const texBlock = material1.getBlockByName("Texture") as TextureBlock;
        texBlock.texture = inputTex;
        material1.backFaceCulling = false;
        const worldPosVarName = (material1.getBlockByName("WorldPos")! as any)
            .output.associatedVariableName;
        const alphaVarName = (material1.getBlockByName("myalpha")! as any)
            .output.associatedVariableName;

        material1.shadowDepthWrapper = new ShadowDepthWrapper(
            material1,
            this.scene,
            {
                remappedVariables: [
                    "worldPos",
                    worldPosVarName,
                    "alpha",
                    alphaVarName,
                ],
            }
        );
        sprite1.material = material1;
        material1.build(true);

        this.shadowGenerator.addShadowCaster(sprite1);

        sprite1.renderingGroupId = 1;

        this.sprite = sprite1;

        // calculate position to place sprite
        const cameraDirection = camera.getDirection(new Vector3(0, 0, 1));
        cameraDirection.y = 0;

        const rotatedCameraDirection = cameraDirection.applyRotationQuaternion(
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
