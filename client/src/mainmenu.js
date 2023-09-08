const MainMenu = (function() {
    // Function to create the main menu GUI
    const create = function(scene) {
        const mainMenu = BABYLON.GUI.AdvancedDynamicTexture.CreateFullscreenUI("UI");
        
        // Adding the background image to the mainMenu
        const backgroundImage = new BABYLON.GUI.Image("backgroundImage", "assets/menu_background.jpg");
        backgroundImage.width = 1;  // Relative width, covering the full width of the GUI
        backgroundImage.height = 1; // Relative height, covering the full height of the GUI
        backgroundImage.stretch = BABYLON.GUI.Image.STRETCH_FILL; // Stretch the image to fill the entire GUI
        mainMenu.addControl(backgroundImage); // Ensure this is the first control added, so it's in the background

        const buttonWidth = "150px";
        const buttonHeight = "40px";
        
        // Header - Gutenverse
        const header = new BABYLON.GUI.TextBlock();
        header.text = "Gutenverse";
        header.height = "80px";
        header.color = "white";
        header.textHorizontalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_CENTER;
        header.fontSize = "48px";
        header.top = "-150px"
        mainMenu.addControl(header); 

        // Function to create a standardized button
        const createButton = function(name, text, topOffset, callback) {
            const button = BABYLON.GUI.Button.CreateSimpleButton(name, text);
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
            console.log("Choose Story clicked");
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
    };

    return {
        create: create
    };
})();
