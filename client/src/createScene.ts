import { Mesh, ShadowGenerator } from "@babylonjs/core";
import type { Scene } from "@babylonjs/core/scene";

export interface SceneArgs {
    scene: Scene;
    shadowGenerator: ShadowGenerator;
    canvas: HTMLCanvasElement;
    world: Mesh;
    stage: Mesh;
}

export interface SceneClass {
    populate: (sceneArgs: SceneArgs) => Promise<Scene>;
    dispose: (sceneArgs: SceneArgs) => void;
}

export type Callback = () => void;