import { Engine } from "@babylonjs/core/Engines/engine";
import "@babylonjs/core/Engines/WebGPU/Extensions/engine.uniformBuffer";
import {
    ArcRotateCamera,
    Constants,
    DefaultRenderingPipeline,
    DirectionalLight,
    MeshBuilder,
    NodeMaterial,
    Scene,
    ShadowGenerator,
    StandardMaterial,
    Texture,
    Vector3,
} from "@babylonjs/core";
import { StartScreen } from "./scenes/startScreen";

import testRamp from "../public/assets/testramp.png";

const DEBUG = false;

import storyContent from "../public/assets/scenes/princessAndDragon.json";
import { StoryPlayer } from "./scenes/storyPlayer";

export const babylonInit = async (): Promise<void> => {
    const canvas = document.getElementById("renderCanvas") as HTMLCanvasElement;
    const engine = new Engine(canvas, true);

    const scene = new Scene(engine);
    const camera = new ArcRotateCamera(
        "playerCamera",
        -Math.PI / 2,
        1.53,
        45,
        new Vector3(0, 10, 0),
        scene
    );

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

    camera.attachControl(canvas, true);
    camera.lowerRadiusLimit = 10;
    camera.upperRadiusLimit = 80;
    camera.lowerBetaLimit = 0;
    camera.upperBetaLimit = 1.8;

    const sphere = MeshBuilder.CreateSphere("world", { diameter: 200 }, scene);
    const material = new StandardMaterial("world", scene);
    sphere.scaling = new Vector3(-1, -1, -1);
    material.backFaceCulling = false;
    sphere.material = material;
    sphere.position.y += 30;

    const dirLight = new DirectionalLight(
        "dirLight",
        camera.getDirection(new Vector3(0, -1, 1)),
        scene
    );
    dirLight.position = camera.position.add(new Vector3(0, 5, 0));
    dirLight.intensity = 0.2;
    dirLight.shadowMinZ = 10;
    dirLight.shadowMaxZ = 100;

    const shadows = new ShadowGenerator(1024, dirLight);
    shadows.transparencyShadow = true;
    shadows.enableSoftTransparentShadow = true;
    shadows.useContactHardeningShadow = true;

    const stage = MeshBuilder.CreateGround("stage", {width: 100, height: 100}, scene);
    stage.material = new StandardMaterial("stage", scene);
    (stage.material as StandardMaterial).opacityTexture = new Texture(testRamp);

    const postProcessing2Mat = await NodeMaterial.ParseFromSnippetAsync(
        "#JQWFX3"
    );
    const postProcessing2 = postProcessing2Mat.createPostProcess(
        camera,
        1.0,
        Constants.TEXTURE_LINEAR_LINEAR
    );

    const postProcessing = new DefaultRenderingPipeline(
        "default",
        true,
        scene,
        [camera]
    );
    postProcessing.grainEnabled = true;
    postProcessing.grain.animated = false;
    postProcessing.grain.intensity = 15;

    const sceneArgs = {
        scene,
        shadowGenerator: shadows,
        canvas,
        world: sphere,
        stage
    };

    // populate initially with main menu
    const startScreen = new StartScreen();
    await startScreen.populate(sceneArgs);

    // JUST FOR TESTING. Not needed for anything else
    (window as any).scene = scene;

    // Register a render loop to repeatedly render the scene
    engine.runRenderLoop(function () {
        scene.render();
    });

    // Watch for browser/canvas resize events
    window.addEventListener("resize", function () {
        engine.resize();
    });
};

babylonInit().then(() => {
    // scene started rendering, everything is initialized
});
