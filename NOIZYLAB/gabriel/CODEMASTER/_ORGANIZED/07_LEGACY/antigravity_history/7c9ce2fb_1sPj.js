// neural-link.js
// THE NEURAL LINK // DIRECT COMMAND INTERFACE
// "Your words are code."

class NeuralLink {
    constructor() {
        this.active = true;
        this.input = document.getElementById('neuralInput');
        this.output = document.getElementById('neuralOutput');
        
        if (this.input) {
            this.input.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') {
                    this.execute(this.input.value);
                    this.input.value = '';
                }
            });
        }
    }

    execute(command) {
        const cmd = command.toLowerCase().trim();
        this.log(`> ${command}`);
        
        // AUDIO FEEDBACK
        if (window.AudioSys) window.AudioSys.playTone(600, 'square', 0.1);

        // COMMAND PARSER
        if (cmd.includes('fix') || cmd.includes('optimize')) {
            window.Gabriel.assist();
            this.log("EXECUTING: OPTIMIZATION PROTOCOL");
        } 
        else if (cmd.includes('dump') || cmd.includes('memory')) {
            window.Gabriel.accessMemory();
            this.log("EXECUTING: MEMORY DUMP");
        }
        else if (cmd.includes('reset') || cmd.includes('clear')) {
            document.getElementById('clearCanvas').click();
            this.log("SYSTEM PURGED.");
        }
        else if (cmd.includes('status')) {
            this.log("SYSTEM STATUS: 100% // TRINITY ONLINE");
            if (window.Rob) window.Rob.speak("All systems functioning within parameters.");
        }
        else {
            // Check for Era switching
            const eras = Object.keys(window.artDirector.eras);
            let found = false;
            eras.forEach(era => {
                if (cmd.includes(era) || cmd.includes(era.replace('_', ' '))) {
                    document.getElementById('directorEra').value = era;
                    this.log(`SHIFTING PARADIGM: ${era.toUpperCase()}`);
                    window.Gabriel.directorMock.generateBrief(era); // Trigger generation
                    found = true;
                }
            });

            if (!found) {
                // If not an era, ask Gabriel/Rob to chat
                if (window.Rob) window.Rob.speak(command); // Echo/Speak
                this.log("TRANSMITTING TO HOST...");
            }
        }
    }

    log(text) {
        if (!this.output) return;
        const line = document.createElement('div');
        line.innerText = text;
        this.output.appendChild(line);
        this.output.scrollTop = this.output.scrollHeight;
    }
}

// Initialize after load
window.addEventListener('load', () => {
    window.NeuralLink = new NeuralLink();
});
