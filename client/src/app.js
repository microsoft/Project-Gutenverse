// Get the canvas element and the engine
const canvas = document.getElementById("renderCanvas");
const engine = new BABYLON.Engine(canvas, true);

// Create the main scene
const createScene = function() {
    const scene = new BABYLON.Scene(engine);

    // Set up a basic camera and light
    const camera = new BABYLON.ArcRotateCamera("Camera", Math.PI / 2, Math.PI / 2, 2, new BABYLON.Vector3(0,0,0), scene);
    camera.attachControl(canvas, true);
    new BABYLON.HemisphericLight("light", new BABYLON.Vector3(0, 1, 0), scene);

    // Create the main menu
    MainMenu.create(scene);

    return scene;
};

// Call the createScene function
const scene = createScene();

// Render loop
engine.runRenderLoop(function() {
    scene.render();
});

// Handle browser resize
window.addEventListener("resize", function() {
    engine.resize();
});
