import { ArcRotateCamera, Color3, Constants, DefaultRenderingPipeline, DirectionalLight, Engine, MeshBuilder, NodeMaterial, Scene, ShadowGenerator, Sound, StandardMaterial, Texture, Vector3 } from "@babylonjs/core";
import { CreateSceneClass } from "../createScene";


import { Player, TextFormat } from "../lib/player";
import { Character, CharacterData } from "../lib/characters";

import paperBg from "../../assets/paperbg.jpg";
import testRamp from "../../assets/testramp.png";

const DEBUG = true;

export class BasicStorybookScene implements CreateSceneClass {
    public characters: CharacterData[];
    public speech: TextFormat[];
    public envUrl: string;
    public nextScene: string;
    public previousScene: string;
    public preTasks?: Promise<unknown>[] | undefined = undefined;
    public soundUrl: string | undefined = undefined;
    public sound?: Sound | undefined = undefined;

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
        scene.fogEnabled = true;
        scene.fogMode = Scene.FOGMODE_EXP2;
        scene.fogDensity = 0.005;
        scene.fogColor = new Color3(0.9, 0.9, 0.85);

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
            -Math.PI / 2,
            1.53,
            45,
            new Vector3(0, 10, 0),
            scene
        );

        camera.attachControl(canvas, true);
        camera.lowerRadiusLimit = 10;
        camera.upperRadiusLimit = 80;
        camera.lowerBetaLimit = 0;
        camera.upperBetaLimit = 1.8;

        const texture = new Texture(this.envUrl);

        const sphere = MeshBuilder.CreateSphere('world', { diameter: 200 }, scene)
        const material = new StandardMaterial('world', scene);
        sphere.scaling = new Vector3(-1, -1, -1);
        material.emissiveTexture = texture;
        material.backFaceCulling = false;
        sphere.material = material;
        sphere.position.y += 50;

        const dirLight = new DirectionalLight("dirLight", camera.getDirection(new Vector3(0, -1, 1)), scene);
        dirLight.position = camera.position.add(new Vector3(0, 5, 0));
        dirLight.intensity = 0.2;
        dirLight.shadowMinZ = 10;
        dirLight.shadowMaxZ = 100;

        const shadows = new ShadowGenerator(1024, dirLight);
        shadows.transparencyShadow = true;
        shadows.enableSoftTransparentShadow = true;
        shadows.useContactHardeningShadow = true;

        for (const character of this.characters) {
            const char = new Character(character, scene, shadows);
            await char.build(camera);
        }
        if (this.soundUrl) {
            this.sound = new Sound("sound", this.soundUrl, scene, null);
        }
        const gui = new Player(scene, this.speech, this.previousScene, this.nextScene, this.sound);

        const floor = MeshBuilder.CreateGround("floor", {width: 100, height: 100});
        const floorMaterial = new StandardMaterial("floorMat", scene);
        floor.material = floorMaterial;
        floor.receiveShadows = true;
        floorMaterial.emissiveTexture = new Texture(paperBg, scene);
        floorMaterial.opacityTexture = new Texture(testRamp, scene);

        
        const postProcessing2Mat = await NodeMaterial.ParseFromSnippetAsync("#JQWFX3");
        const postProcessing2 = postProcessing2Mat.createPostProcess(camera, 1.0, Constants.TEXTURE_LINEAR_LINEAR);
        
        const postProcessing = new DefaultRenderingPipeline("default", true, scene, [camera]);
        postProcessing.grainEnabled = true;
        postProcessing.grain.animated = false;
        postProcessing.grain.intensity = 15;

        return scene;
    };
}