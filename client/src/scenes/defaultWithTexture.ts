import { Engine } from "@babylonjs/core/Engines/engine";
import { Scene } from "@babylonjs/core/scene";
import { ArcRotateCamera } from "@babylonjs/core/Cameras/arcRotateCamera";
import { Vector3 } from "@babylonjs/core/Maths/math.vector";
import { CreateSphere } from "@babylonjs/core/Meshes/Builders/sphereBuilder";
import { CreateGround } from "@babylonjs/core/Meshes/Builders/groundBuilder";
import { StandardMaterial } from "@babylonjs/core/Materials/standardMaterial";
import { CreateSceneClass } from "../createScene";

// If you don't need the standard material you will still need to import it since the scene requires it.
// import "@babylonjs/core/Materials/standardMaterial";
import { Texture } from "@babylonjs/core/Materials/Textures/texture";

import grassTextureUrl from "../../assets/grass.jpg";
import { DirectionalLight } from "@babylonjs/core/Lights/directionalLight";
import { ShadowGenerator } from "@babylonjs/core/Lights/Shadows/shadowGenerator";

import "@babylonjs/core/Lights/Shadows/shadowGeneratorSceneComponent";
import { AdvancedDynamicTexture } from "@babylonjs/gui/2D/advancedDynamicTexture";
import { Image } from "@babylonjs/gui/2D/controls/image";
import { TextBlock } from "@babylonjs/gui/2D/controls/textBlock";
import { Control } from "@babylonjs/gui/2D/controls/control";
import {Button } from "@babylonjs/gui/2D/controls/button";

import menuBackgroundUrl from "../../assets/menu_background.jpg";

export class DefaultSceneWithTexture implements CreateSceneClass {
    createScene = async (
        engine: Engine,
        canvas: HTMLCanvasElement
    ): Promise<Scene> => {
        // This creates a basic Babylon Scene object (non-mesh)
        const scene = new Scene(engine);

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

        // This creates and positions a free camera (non-mesh)
        const camera = new ArcRotateCamera(
            "my first camera",
            0,
            Math.PI / 3,
            10,
            new Vector3(0, 0, 0),
            scene
        );

        // This targets the camera to scene origin
        camera.setTarget(Vector3.Zero());

        // This attaches the camera to the canvas
        camera.attachControl(canvas, true);

        const mainMenu = AdvancedDynamicTexture.CreateFullscreenUI("UI");
        
        // Adding the background image to the mainMenu
        const backgroundImage = new Image("backgroundImage", menuBackgroundUrl);
        backgroundImage.width = 1;  // Relative width, covering the full width of the GUI
        backgroundImage.height = 1; // Relative height, covering the full height of the GUI
        backgroundImage.stretch = Image.STRETCH_FILL; // Stretch the image to fill the entire GUI
        mainMenu.addControl(backgroundImage); // Ensure this is the first control added, so it's in the background

        const buttonWidth = "150px";
        const buttonHeight = "40px";
        
        // Header - Gutenverse
        const header = new TextBlock();
        header.text = "Gutenverse";
        header.height = "80px";
        header.color = "white";
        header.textHorizontalAlignment = Control.HORIZONTAL_ALIGNMENT_CENTER;
        header.fontSize = "48px";
        header.top = "-150px"
        mainMenu.addControl(header); 

        // Function to create a standardized button
        const createButton = function(name: string, text: string, topOffset: string, callback: () => void) {
            const button = Button.CreateSimpleButton(name, text);
            button.width = buttonWidth;
            button.height = buttonHeight;
            button.color = "black";
            button.cornerRadius = 5;
            button.background = "lightgray"; // Set the background color to light gray
            button.top = topOffset;
            button.onPointerUpObservable.add(callback);
            mainMenu.addControl(button);
            return button;
        }

        // Choose Story Button
        createButton("chooseStory", "Choose Story", "-100px", function() {
            //console.log("Choose Story clicked");
            window.location.href += "?scene=loadModelAndEnv"; 
        });

        // Create Story Button
        createButton("createStory", "Create Story", "-50px", function() {
            console.log("Create Story clicked");
        });

        // Settings Button (Stub for now)
        createButton("settings", "Settings", "0px", function() {
            console.log("Settings clicked");
        });

        // Exit Button
        createButton("exit", "Exit", "50px", function() {
            window.close();
        });

        // This creates a light, aiming 0,1,0 - to the sky (non-mesh)
        // const light = new HemisphericLight(
        //     "light",
        //     new Vector3(0, 1, 0),
        //     scene
        // );

        // // Default intensity is 1. Let's dim the light a small amount
        // light.intensity = 0.7;

        // // Our built-in 'sphere' shape.
        // const sphere = CreateSphere(
        //     "sphere",
        //     { diameter: 2, segments: 32 },
        //     scene
        // );

        // // Move the sphere upward 1/2 its height
        // sphere.position.y = 1;

        // // Our built-in 'ground' shape.
        // const ground = CreateGround(
        //     "ground",
        //     { width: 6, height: 6 },
        //     scene
        // );

        // // Load a texture to be used as the ground material
        // const groundMaterial = new StandardMaterial("ground material", scene);
        // groundMaterial.diffuseTexture = new Texture(grassTextureUrl, scene);

        // ground.material = groundMaterial;
        // ground.receiveShadows = true;

        // const light = new DirectionalLight(
        //     "light",
        //     new Vector3(0, -1, 1),
        //     scene
        // );
        // light.intensity = 0.5;
        // light.position.y = 10;

        // const shadowGenerator = new ShadowGenerator(512, light)
        // shadowGenerator.useBlurExponentialShadowMap = true;
        // shadowGenerator.blurScale = 2;
        // shadowGenerator.setDarkness(0.2);

        // shadowGenerator.getShadowMap()!.renderList!.push(sphere);

        return scene;
    };
}

export default new DefaultSceneWithTexture();
