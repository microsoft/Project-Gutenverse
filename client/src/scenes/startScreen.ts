// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

import { Scene } from "@babylonjs/core/scene";
import { Callback, SceneArgs, SceneClass } from "../createScene";
import { AdvancedDynamicTexture } from "@babylonjs/gui/2D/advancedDynamicTexture";
import { Image } from "@babylonjs/gui/2D/controls/image";
import { TextBlock } from "@babylonjs/gui/2D/controls/textBlock";
import { TextWrapping } from "@babylonjs/gui/2D/controls/textBlock"
import { Control } from "@babylonjs/gui/2D/controls/control";
import {Button } from "@babylonjs/gui/2D/controls/button";
import { InputTextArea } from "@babylonjs/gui/2D/controls/inputTextArea"
import { Grid } from "@babylonjs/gui/2D/controls/grid"
import { StackPanel } from "@babylonjs/gui/2D/controls/stackPanel"
import { ScrollViewer } from "@babylonjs/gui/2D/controls/scrollViewers/scrollViewer"
import * as StatusPanel from "../StatusPanel";

import menuBackgroundUrl from "../../public/assets/menu_background.jpg";
import normalButtonBackgroundUrl from "../../public/assets/textures/old_paper_texture_01.png";
import storyButtonBackgroundUrl from "../../public/assets/textures/old_paper_texture_02.png";
import blackButtonBackgroundUrl from "../../public/assets/textures/black_paper_texture_01.png"
import { StoryPlayer } from "./storyPlayer";
import { GetClass, RegisterClass } from "@babylonjs/core";

export class StartScreen implements SceneClass {

    public gui?: AdvancedDynamicTexture;
    populate = async (
        sceneArgs: SceneArgs
    ): Promise<Scene> => {
        const scene = sceneArgs.scene;
        // const advancedTexture = AdvancedDynamicTexture.CreateFullscreenUI("UI", true, scene);
        console.log('grid get', GetClass("BABYLON.GUI.Grid"));
        RegisterClass("BABYLON.GUI.Grid", Grid);
        RegisterClass("BABYLON.GUI.ScrollViewer", ScrollViewer);
        fetch("http://127.0.0.1:5000/latest-story").then(latestResp => {
            latestResp.json().then(guidData => {
                // const panel: StatusPanel.StatusPanel = new StatusPanel.StatusPanel(guidData.latest_folder);
            })
        });
        await AdvancedDynamicTexture.ParseFromSnippetAsync("#HHCQ02#67").then((gui) => {
            this.gui = gui;

            // We need to create the text input field, as it is used in other functions
            const intputTextDefault = "Create a story";
            const inputTextContainer = gui.getControlByName("CreateStoryGrid")! as Grid;

            const inputNameArea = gui.getControlByName("InputText_Name")! as InputTextArea;

            const inputTextArea = new InputTextArea('Example InputTextArea', intputTextDefault);
            inputTextArea.width = "99%";
            inputTextArea.height = "80%";
            inputTextArea.color = "white";
            inputTextArea.thickness = 0;

            inputTextContainer.addControl(inputTextArea, 2, 0);

            // Add Background Image
            const backgroundImage = new Image("backgroundImage", menuBackgroundUrl);
            backgroundImage.width = 1;  // Relative width, covering the full width of the GUI
            backgroundImage.height = 1; // Relative height, covering the full height of the GUI
            backgroundImage.stretch = Image.STRETCH_FILL; // Stretch the image to fill the entire GUI
            const backgroundImageContainer =  gui.getControlByName("BackgroundImageGrid")! as Grid;
            backgroundImageContainer.addControl(backgroundImage);

            const uploadButton = gui.getControlByName("Button_CreateStoryLaunch");
            uploadButton?.onPointerClickObservable.addOnce(() => {
                // Extract title and body from input fields
                const storyTitle = inputNameArea.text;
                const storyBody = inputTextArea.text;

                // Create the JSON payload
                const payload = {
                    "title": storyTitle,
                    "body": storyBody
                };

                // Send POST request
                fetch('http://localhost:5000/stories', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload)
                }).then(response => response.json())
                .then(data => {

                })
                .catch(error => console.error('Error:', error));
                alert("Upload started!")
            });

            // === MAIN MENU ===
            
            // Get all of the menus and sub-menus
            const mainMenu = gui.getControlByName("MainMenuGrid")!;
            const exitMenu = gui.getControlByName("ExitMenuGrid")!;
            const mainMenuDefaultOptions = gui.getControlByName("StackPanel_MainMenu")!;
            const chooseStoryMenu = gui.getControlByName("ChooseStoryGrid")!;
            const createStoryMenu = gui.getControlByName("CreateStoryGrid")!;

            const setupButtonVisuals = function(button: Button, title: string, fontColor: string, fontFamly: string, fontSize: number, isBold: boolean, url:  "*.jpg" | "*.png"){
                // Make image first, so the text appears in front of it
                var buttonImage = new Image("buttonImage", url);
                buttonImage.width = 1;
                buttonImage.height = 1;
                buttonImage.stretch = Image.STRETCH_FILL;
                button.thickness = 0;
                button.addControl(buttonImage);

                // Now make the text
                var buttonText = new TextBlock("text_" + title, title);
                buttonText.width = "100.00%";
                buttonText.height =  "100.00%";
                buttonText.color = fontColor;
                buttonText.fontFamily = fontFamly;
                buttonText.fontSize = fontSize;
                buttonText.fontWeight
                buttonText.textWrapping = TextWrapping.Ellipsis;

                if (isBold) {
                    buttonText.fontWeight = "bold";
                }
                button.addControl(buttonText);

                return buttonText;
            }

            const btnFontWhite = "white";
            const btnFontBlack = "black";
            const btnFontFamily = "MV Boli";
            const btnSmallFontSize = 22;
            const btnLargeFontSize = 35;
            const btnIsBold = false;

            const rootGrid =  gui.getControlByName("RootGrid")! as Control;

            // Setup the buttons in Main menu
            const button_mainMenuChooseStoryButton = gui.getControlByName("Button_MainMenu_ChooseStory")! as Button;
            setupButtonVisuals(button_mainMenuChooseStoryButton, "Choose Story", btnFontBlack, btnFontFamily, btnLargeFontSize, btnIsBold, normalButtonBackgroundUrl);

            const button_mainMenuCreateStoryButton = gui.getControlByName("Button_MainMenu_CreateStory")! as Button;
            setupButtonVisuals(button_mainMenuCreateStoryButton, "Create Story", btnFontBlack, btnFontFamily, btnLargeFontSize, btnIsBold, normalButtonBackgroundUrl);

            const button_mainMenuExitButton = gui.getControlByName("Button_MainMenu_Exit")! as Button;
            setupButtonVisuals(button_mainMenuExitButton, "Exit", btnFontBlack, btnFontFamily, btnLargeFontSize, btnIsBold, normalButtonBackgroundUrl);
            
            const button_mainMenuExitConfirmButton = gui.getControlByName("Button_ConfirmExit")! as Button;
            setupButtonVisuals(button_mainMenuExitConfirmButton, "Yes", btnFontBlack, btnFontFamily, btnLargeFontSize, btnIsBold, normalButtonBackgroundUrl);

            const button_mainMenuExitCancelButton = gui.getControlByName("Button_CancelExit")! as Button;
            setupButtonVisuals(button_mainMenuExitCancelButton, "No", btnFontBlack, btnFontFamily, btnLargeFontSize, btnIsBold, normalButtonBackgroundUrl);
            
            const button_createStory = gui.getControlByName("Button_CreateStoryLaunch")! as Button;
            setupButtonVisuals(button_createStory, "Upload", btnFontBlack, btnFontFamily, btnLargeFontSize, btnIsBold, normalButtonBackgroundUrl);

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
                inputNameArea.text = "Name";
                inputTextArea.text = intputTextDefault;
            }

            const quit = function() {
                window.close();
            }
            
            button_mainMenuChooseStoryButton.onPointerUpObservable.add(openChooseStoryMenu);
            button_mainMenuCreateStoryButton.onPointerUpObservable.add(openCreateStoryMenu);
            button_mainMenuExitButton.onPointerUpObservable.add(openExitMenu);
            button_mainMenuExitConfirmButton.onPointerUpObservable.add(quit);
            button_mainMenuExitCancelButton.onPointerUpObservable.add(openMainMenu);

            // === CHOOSE STORY MENU ===

            // Setup the buttons in the Choose Story menu
            const button_closeMenuChooseStory = gui.getControlByName("Button_Close_ChooseStory")! as Button;
            setupButtonVisuals(button_closeMenuChooseStory, "Back", btnFontWhite, btnFontFamily, btnSmallFontSize, false, blackButtonBackgroundUrl);
            button_closeMenuChooseStory.onPointerUpObservable.add(openMainMenu);

            const stackButtonContainer = gui.getControlByName("StackPanel_StoryButtons")! as StackPanel;
            function fixCharacterContinuity(scenesJson: any): any {
                const characterImageUrlMap: { [key: string]: string } = {};
              
                scenesJson.scenes.forEach((scene: any) => {
                  scene.characters.forEach((character: any) => {
                    if (character.name && character.imageUrl) {
                      if (!characterImageUrlMap[character.name]) {
                        characterImageUrlMap[character.name] = character.imageUrl;
                      } else {
                        character.imageUrl = characterImageUrlMap[character.name];
                      }
                    }
                  });
                });
              
                return scenesJson;
              }
            const storyRequest = fetch("http://127.0.0.1:5000/stories/disk");
            storyRequest.then(response => {
                if (!response.ok) {
                    throw new Error("Failed to fetch stories.");
                }
                const storiesPromise = response.json();
                storiesPromise.then(stories => {
                    // Assuming there's a container (like a StackPanel or other container control) where you want to add the buttons
                    const storyButtonContainer = new StackPanel();
        
                    //Iterating through the fetched stories and creating buttons
                    stories.forEach((story: {Id: string, Title: string} )=> {
                        //const storyButton = Button.CreateSimpleButton(story.Id, story.Title);
                        const storyButton = new Button(story.Id);
                        const storyId: string = story.Id;
                        storyButton.width = "95%";
                        storyButton.height = "60px";
                        storyButton.cornerRadius = 6;
                        setupButtonVisuals(storyButton, story.Title, btnFontBlack, btnFontFamily, btnLargeFontSize, btnIsBold, storyButtonBackgroundUrl);

                        storyButton.onPointerUpObservable.add(() => {
                            const storyRequest = fetch("http://127.0.0.1:5000/stories/" + storyId + "/scene");
                            storyRequest.then(response => {
                                if (!response.ok) {
                                    throw new Error("Failed to fetch scenes for story: " + storyId);
                                }

                                const scenesPromise = response.json();
                                scenesPromise.then(scenes => {
                                    console.log(scenes);
                                    rootGrid.isVisible = false;
                                    backgroundImage.isVisible = false;

                                    gui.dispose();
                                    fixCharacterContinuity(scenes);
                                    const player: StoryPlayer = new StoryPlayer(scenes, sceneArgs);
                                    player.playScene();
                                });
                            });
                        });
        
                        storyButtonContainer.addControl(storyButton);
                    });
                    // Assuming you have a GUI texture where you want to add the container
                    stackButtonContainer.addControl(storyButtonContainer);    
                })
                
            });
            
            // === CREATE STORY MENU ===

            // Setup the buttons in the Create Story menu
            const button_closeMenuCreateStory = gui.getControlByName("Button_Close_CreateStory")! as Button;
            setupButtonVisuals(button_closeMenuCreateStory, "Back", btnFontWhite, btnFontFamily, btnSmallFontSize, false, blackButtonBackgroundUrl);
            button_closeMenuCreateStory.onPointerUpObservable.add(openMainMenu);
            
        });

        return scene;
    };

    dispose() {
        if (this.gui) {
            this.gui.dispose();
        }
    }
}
