export class StatusPanel {
    private guid: string;
    private panel: HTMLElement | null;
    private intervalId: number | undefined;
    
    constructor(guid: string) {
        this.guid = guid;
        this.panel = null;
        this.createPanel();
        this.updateStatus();
        this.intervalId = window.setInterval(() => this.updateStatus(), 30000);
    }
    
    private createPanel(): void {
        const panel = document.createElement('div');
        panel.style.position = 'fixed';
        panel.style.top = '0';
        panel.style.left = '0';
        panel.style.backgroundColor = 'white';
        panel.style.border = '1px solid black';
        panel.style.padding = '10px';
        document.body.appendChild(panel);
        this.panel = panel;
    }
    
    private async updateStatus(): Promise<void> {
        try {
            const response = await fetch(`http://localhost:5000/stories/${this.guid}/status`);
            const data = await response.json();
            
            if (data["Current Scene and Stage"] === "Complete") {
                this.dispose();
                return;
            }
            
            if (this.panel) {
                this.panel.textContent = `Pipeline Status:  ${data["Current Scene and Stage"]}
                Number of Scenes: ${data["Number of Scenes"]}
                Stages Left: ${data["Stages Left"].join(', ')}
                `;
            }
        } catch (error) {
            console.error("Error fetching status:", error);
        }
    }
    
    private dispose(): void {
        if (this.panel) {
            this.panel.remove();
        }
        if (this.intervalId !== undefined) {
            window.clearInterval(this.intervalId);
        }
    }
}