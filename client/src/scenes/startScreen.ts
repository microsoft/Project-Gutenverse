import { Scene } from "@babylonjs/core/scene";
import { Callback, SceneArgs, SceneClass } from "../createScene";
import { AdvancedDynamicTexture } from "@babylonjs/gui/2D/advancedDynamicTexture";
import { Image } from "@babylonjs/gui/2D/controls/image";
import { TextBlock } from "@babylonjs/gui/2D/controls/textBlock";
import { Control } from "@babylonjs/gui/2D/controls/control";
import {Button } from "@babylonjs/gui/2D/controls/button";

import menuBackgroundUrl from "../../public/assets/menu_background.jpg";

export interface StartScreenArgs {
    chooseStoryCallback: Callback;
}

export class StartScreen implements SceneClass {
    public gui?: AdvancedDynamicTexture;
    constructor(public startScreenArgs: StartScreenArgs) {}
    populate = async (
        sceneArgs: SceneArgs
    ): Promise<Scene> => {
        const scene = sceneArgs.scene;
        
        const mainMenu = AdvancedDynamicTexture.CreateFullscreenUI("UI");
        this.gui = mainMenu;
        
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
        createButton("chooseStory", "Choose Story", "-100px", () => {
            this.startScreenArgs.chooseStoryCallback(); 
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

        return scene;
    };

    dispose() {
        if (this.gui) {
            this.gui.dispose();
        }
    }
}
