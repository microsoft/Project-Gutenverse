import { ArcRotateCamera, Color4, DefaultRenderingPipeline, DirectionalLight, Engine, MeshBuilder, Scene, ShadowGenerator, StandardMaterial, Texture, Tools, Vector3 } from "@babylonjs/core";
import { CreateSceneClass } from "../createScene";


import { Player, TextFormat } from "../lib/player";
import { Character, CharacterData } from "../lib/characters";

const DEBUG = false;

export class BasicStorybookScene implements CreateSceneClass {
    public characters: CharacterData[];
    public speech: TextFormat[];
    public envUrl: string;
    public nextScene: string;
    public previousScene: string;
    public preTasks?: Promise<unknown>[] | undefined = undefined;

    constructor() {
        this.characters = [];
        this.speech = [];
        this.envUrl = "";
        this.nextScene = "";
        this.previousScene = "";
    }

    createScene = async (
        engine: Engine,
        canvas: HTMLCanvasElement
    ): Promise<Scene> => {
        // This creates a basic Babylon Scene object (non-mesh)
        const scene = new Scene(engine);
        scene.clearColor = new Color4(0, 0, 0, 0);
        if (DEBUG) {
            void Promise.all([
                import("@babylonjs/core/Debug/debugLayer"),
                import("@babylonjs/inspector"),
            ]).then((_values) => {
                console.log(_values);
                scene.debugLayer.show({
                    handleResize: true,
                    overlay: true,
                    globalRoot: document.getElementById("#root") || undefined,
                });
            });
        }

        // This creates and positions a free camera (non-mesh)
        const camera = new ArcRotateCamera(
            "playerCamera",
            -0.574,
            1.334,
            22,
            new Vector3(0.43, -1.15, -0.2),
            scene
        );

        // This attaches the camera to the canvas
        camera.attachControl(canvas, true);

        // we'll change the env with the scene later
        const texture = new Texture(this.envUrl);

        const sphere = MeshBuilder.CreateSphere('world', { diameter: 100 }, scene)
        const material = new StandardMaterial('world', scene)
        sphere.scaling = new Vector3(-1, -1, -1)
        material.emissiveTexture = texture
        material.backFaceCulling = false
        sphere.material = material

        const dirLight = new DirectionalLight("dirLight", new Vector3(-1, -1, 0), scene);
        dirLight.position.set(1, 20, 0);
        dirLight.intensity = 0.2;
        dirLight.shadowMinZ = 5;
        dirLight.shadowMaxZ = 30;

        const shadows = new ShadowGenerator(1024, dirLight);
        sphere.receiveShadows = true;
        shadows.transparencyShadow = true;
        shadows.enableSoftTransparentShadow = true;
        shadows.useContactHardeningShadow = true;

        for (const character of this.characters) {
            const char = new Character(character, scene, shadows);
            await char.build();
        }

        const gui = new Player(scene, this.speech, this.previousScene, this.nextScene);

        const postProcessing = new DefaultRenderingPipeline("default", true, scene, [camera]);
        postProcessing.grainEnabled = true;
        postProcessing.grain.animated = true;
        postProcessing.grain.intensity = 15;

        return scene;
    };
}