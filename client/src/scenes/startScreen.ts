import { Scene } from "@babylonjs/core/scene";
import { Callback, SceneArgs, SceneClass } from "../createScene";
import { AdvancedDynamicTexture } from "@babylonjs/gui/2D/advancedDynamicTexture";
import { Image } from "@babylonjs/gui/2D/controls/image";
import { TextBlock } from "@babylonjs/gui/2D/controls/textBlock";
import { Control } from "@babylonjs/gui/2D/controls/control";
import {Button } from "@babylonjs/gui/2D/controls/button";
import { InputTextArea } from "@babylonjs/gui/2D/controls/inputTextArea"
import { Grid } from "@babylonjs/gui/2D/controls/grid"

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
        const advancedTexture = AdvancedDynamicTexture.CreateFullscreenUI("UI", true, scene);

        // TODO: Add background image

        const backgroundImage = new Image("backgroundImage", menuBackgroundUrl);
        backgroundImage.width = 1;  // Relative width, covering the full width of the GUI
        backgroundImage.height = 1; // Relative height, covering the full height of the GUI
        backgroundImage.stretch = Image.STRETCH_FILL; // Stretch the image to fill the entire GUI
        advancedTexture.addControl(backgroundImage); // Ensure this is the first control added, so it's in the background

        await AdvancedDynamicTexture.ParseFromSnippetAsync("#HHCQ02#38").then((gui) => {
            this.gui = advancedTexture;

            // SECTION 1: MAIN MENU
            // Get all of the menus and sub-menus
            const mainMenu = gui.getControlByName("MainMenuGrid")!;
            const exitMenu = gui.getControlByName("ExitMenuGrid")!;
            const mainMenuDefaultOptions = gui.getControlByName("StackPanel_MainMenu")!;
            const chooseStoryMenu = gui.getControlByName("ChooseStoryGrid")!;
            const createStoryMenu = gui.getControlByName("CreateStoryGrid")!;

            // Setup the buttons in Main menu
            const button_mainMenuChooseStoryButton = gui.getControlByName("Button_MainMenu_ChooseStory")! as Button;
            const button_mainMenuCreateStoryButton = gui.getControlByName("Button_MainMenu_CreateStory")! as Button;
            const button_mainMenuExitButton = gui.getControlByName("Button_MainMenu_Exit")! as Button;
            const button_mainMenuExitConfirmButton = gui.getControlByName("Button_ConfirmExit")! as Button;
            const button_mainMenuExitCancelButton = gui.getControlByName("Button_CancelExit")! as Button;

            const openMainMenu = function(){
                mainMenu.isVisible = true;
                exitMenu.isVisible = false;
                mainMenuDefaultOptions.isVisible = true;
                chooseStoryMenu.isVisible = false;
                createStoryMenu.isVisible = false;
            }

            const openExitMenu = function(){
                mainMenu.isVisible = true;
                exitMenu.isVisible = true;
                mainMenuDefaultOptions.isVisible = false;
                chooseStoryMenu.isVisible = false;
                createStoryMenu.isVisible = false;
            }
        
            const openChooseStoryMenu = function(){
                mainMenu.isVisible = false;
                chooseStoryMenu.isVisible = true;
                createStoryMenu.isVisible = false;
            }
        
            const openCreateStoryMenu = function(){
                mainMenu.isVisible = false;
                chooseStoryMenu.isVisible = false;
                createStoryMenu.isVisible = true;
            }

            const quit = function() {
                window.close();
            }
            
            button_mainMenuChooseStoryButton.onPointerUpObservable.add(openChooseStoryMenu);
            button_mainMenuCreateStoryButton.onPointerUpObservable.add(openCreateStoryMenu);
            button_mainMenuExitButton.onPointerUpObservable.add(openExitMenu);
            button_mainMenuExitConfirmButton.onPointerUpObservable.add(quit);
            button_mainMenuExitCancelButton.onPointerUpObservable.add(openMainMenu);

            // SECTION 2: CHOOSE STORY MENU

            // Setup the buttons in the Choose Story menu
            const button_closeMenuChooseStory = gui.getControlByName("Button_Close_ChooseStory")!;
            button_closeMenuChooseStory.onPointerUpObservable.add(openMainMenu);

            // SECTION 3: CREATE STORY MENU

            // Setup the buttons in the Create Story menu
            const button_closeMenuCreateStory = gui.getControlByName("Button_Close_CreateStory")!;
            button_closeMenuCreateStory.onPointerUpObservable.add(openMainMenu);

            // Setup text input for create story menu
            const inputTextContainer = gui.getControlByName("CreateStoryGrid")! as Grid;
            const inputTextArea = new InputTextArea('Example InputTextArea', "Create a story");
            inputTextArea.width = "80%";
            inputTextArea.height = "100%";
            inputTextArea.color = "white";
            inputTextContainer.addControl(inputTextArea, 1, 0);
            
        });


        /*
        const mainMenu = AdvancedDynamicTexture.CreateFullscreenUI("UI", true, scene);
        let loadedGUI = await  mainMenu.parseFromSnippetAsync("#HHCQ02#36");
        
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
        */

        return scene;
    };

    dispose() {
        if (this.gui) {
            this.gui.dispose();
        }
    }
}
