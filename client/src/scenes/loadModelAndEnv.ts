import { Engine } from "@babylonjs/core/Engines/engine";
import { Scene } from "@babylonjs/core/scene";
import { ArcRotateCamera } from "@babylonjs/core/Cameras/arcRotateCamera";
import { Vector3 } from "@babylonjs/core/Maths/math.vector";
import { HemisphericLight } from "@babylonjs/core/Lights/hemisphericLight";
import { CreateSceneClass } from "../createScene";
import { SceneLoader } from "@babylonjs/core/Loading/sceneLoader";
import { CubeTexture } from "@babylonjs/core/Materials/Textures/cubeTexture";
import { EnvironmentHelper } from "@babylonjs/core/Helpers/environmentHelper";

// required imports
import "@babylonjs/core/Loading/loadingScreen";
import "@babylonjs/loaders/glTF";
import "@babylonjs/core/Materials/standardMaterial";
import "@babylonjs/core/Materials/Textures/Loaders/envTextureLoader";


// digital assets
import controllerModel from "../../assets/glb/samsung-controller.glb";
import roomEnvironment from "../../assets/environment/room.env"
import { Texture } from "@babylonjs/core/Materials/Textures/texture";
import { MeshBuilder } from "@babylonjs/core/Meshes/meshBuilder";
import { StandardMaterial } from "@babylonjs/core/Materials/standardMaterial";

import environmentUrl from "../../assets/environment/blockade_env.png";
import princessPenguinUrl from "../../assets/characters/princesspenguin.png";
import { PBRMaterial } from "@babylonjs/core/Materials/PBR/pbrMaterial";
import { PointLight } from "@babylonjs/core/Lights/pointLight";

import '@babylonjs/loaders/OBJ/objFileLoader'

export class LoadModelAndEnvScene implements CreateSceneClass {
    createScene = async (
        engine: Engine,
        canvas: HTMLCanvasElement
    ): Promise<Scene> => {
        // This creates a basic Babylon Scene object (non-mesh)
        const scene = new Scene(engine);

        // This creates and positions a free camera (non-mesh)
        const camera = new ArcRotateCamera(
            "my first camera",
            -Math.PI/2,
            0,
            10,
            new Vector3(0, 0, 0),
            scene
        );

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

        // This targets the camera to scene origin
        camera.setTarget(Vector3.Zero());

        // This attaches the camera to the canvas
        camera.attachControl(canvas, true);

        // camera.useFramingBehavior = true;

        const texture = new Texture(environmentUrl);

        const sphere = MeshBuilder.CreateSphere('world', { diameter: 20 }, scene)
        const material = new StandardMaterial('world', scene)
        sphere.scaling = new Vector3(-1, -1, -1)
        material.emissiveTexture = texture
        material.backFaceCulling = false
        sphere.material = material

        // load the environment file
        scene.environmentTexture = new CubeTexture(roomEnvironment, scene);

        // if not setting the envtext of the scene, we have to load the DDS module as well
        new EnvironmentHelper( {
            skyboxTexture: roomEnvironment,
            createGround: false
        }, scene)

        // This creates a light, aiming 0,1,0 - to the sky (non-mesh)
        const light = new HemisphericLight(
            "light",
            new Vector3(0, 1, 0),
            scene
        );

        // Default intensity is 1. Let's dim the light a small amount
        light.intensity = 0.3;

        // const importResult = await SceneLoader.ImportMeshAsync(
        //     "",
        //     "",
        //     controllerModel,
        //     scene,
        //     undefined,
        //     ".glb"
        // );

        // // just scale it so we can see it better
        // importResult.meshes[0].scaling.scaleInPlace(10);

        // set up some sprites?
        const sprite1 = MeshBuilder.CreatePlane("sprite1", { size: 1 }, scene);
        const material1 = new StandardMaterial("mat1", scene);
        material1.diffuseTexture = new Texture(princessPenguinUrl, scene);
        material1.diffuseTexture.hasAlpha = true;
        material1.emissiveTexture = material1.diffuseTexture;
        material1.useAlphaFromDiffuseTexture = true;
        material1.backFaceCulling = false;
        sprite1.material = material1;

        sprite1.position.z = 2;

        // const pl = new PointLight("pl", new Vector3(0, 0, 0), scene);

        return scene;
    };
}

export default new LoadModelAndEnvScene();
