// Browse Library Feature - Simple Implementation

const LIBRARY_TOPICS = [
    // Algorithms
    { name: "Bubble Sort", prompt: "Visualize Bubble Sort", category: "Sorting" },
    { name: "Selection Sort", prompt: "Visualize Selection Sort", category: "Sorting" },
    { name: "Merge Sort", prompt: "Visualize Merge Sort", category: "Sorting" },
    { name: "Quicksort", prompt: "Visualize Quicksort", category: "Sorting" },
    { name: "Binary Search", prompt: "Visualize Binary Search", category: "Search" },
    { name: "BFS", prompt: "Visualize BFS Graph", category: "Graphs" },
    { name: "Dijkstra's Algorithm", prompt: "Visualize Dijkstra's Algorithm", category: "Graphs" },

    // Mathematics
    { name: "Pythagorean Theorem", prompt: "Visualize Pythagoras Theorem", category: "Geometry" },
    { name: "Sine Wave", prompt: "Show Sine Wave", category: "Trigonometry" },
    { name: "Quadratic Roots", prompt: "Show Quadratic formula", category: "Algebra" },
    { name: "Matrix Multiplication", prompt: "Visualize Matrix Multiplication", category: "Linear Algebra" },
    { name: "Calculus Limit", prompt: "Show concept of a Limit", category: "Calculus" },
    { name: "Definite Integral", prompt: "Visualize Integral area", category: "Calculus" },
    { name: "Chain Rule", prompt: "Explain Chain Rule", category: "Calculus" },
    { name: "Fourier Series", prompt: "Show Fourier transform", category: "Advanced Math" },

    // Physics
    { name: "Solar System", prompt: "Show Solar System", category: "Astronomy" },
    { name: "Atom Model", prompt: "Visualize Atom model", category: "Quantum Physics" },
    { name: "Bernoulli's Principle", prompt: "Show Bernoulli's Principle", category: "Fluid Dynamics" },

    // Biology
    { name: "DNA Helix", prompt: "Visualize DNA Helix", category: "Genetics" },
    { name: "Mitosis", prompt: "Show Mitosis steps", category: "Cell Biology" },
    { name: "Photosynthesis", prompt: "Explain Photosynthesis", category: "Botany" },
    { name: "Water Cycle", prompt: "Show Water Cycle", category: "Ecology" },

    // Data Structures
    { name: "Stack", prompt: "Visualize Stack operations", category: "Data Structures" },
    { name: "Queue", prompt: "Visualize Queue operations", category: "Data Structures" },

    // Geometry
    { name: "Basic Shapes", prompt: "Show Geometry shapes", category: "Geometry" },
    { name: "Sphere", prompt: "Show 3D Sphere", category: "3D Geometry" },
    { name: "Triangle", prompt: "Show Triangle properties", category: "Geometry" },
    { name: "Pentagon", prompt: "Show Pentagon", category: "Geometry" },
    { name: "Hexagon", prompt: "Show Hexagon", category: "Geometry" }
];

// Initialize Browse Library
function initBrowseLibrary() {
    const browseBtn = document.getElementById('browseLibBtn');
    const modal = document.getElementById('libModal');
    const closeBtn = document.getElementById('closeLibBtn');
    const searchInput = document.getElementById('libSearch');
    const listContainer = document.getElementById('libList');
    const promptInput = document.getElementById('promptInput');
    const generateBtn = document.getElementById('generateBtn');

    if (!browseBtn || !modal) return;

    // Open modal
    browseBtn.addEventListener('click', () => {
        modal.style.display = 'block';
        renderTopics(LIBRARY_TOPICS);
        if (searchInput) searchInput.focus();
    });

    // Close modal
    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';
        if (searchInput) searchInput.value = '';
    });

    // Close on background click
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
            if (searchInput) searchInput.value = '';
        }
    });

    // Close on ESC key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.style.display === 'block') {
            modal.style.display = 'none';
            if (searchInput) searchInput.value = '';
        }
    });

    // Search functionality
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase();
            const filtered = LIBRARY_TOPICS.filter(topic =>
                topic.name.toLowerCase().includes(query) ||
                topic.category.toLowerCase().includes(query)
            );
            renderTopics(filtered);
        });
    }

    // Render topics
    function renderTopics(topics) {
        if (!listContainer) return;

        listContainer.innerHTML = '';

        if (topics.length === 0) {
            listContainer.innerHTML = '<p style="color:#888; text-align:center; grid-column:1/-1;">No topics found</p>';
            return;
        }

        topics.forEach(topic => {
            const card = document.createElement('div');
            card.style.cssText = 'background:rgba(102,126,234,0.1); border:1px solid rgba(102,126,234,0.3); border-radius:12px; padding:1.2rem; cursor:pointer; transition:all 0.3s;';

            card.innerHTML = `
                <h3 style="color:#667eea; margin:0 0 0.5rem 0; font-size:1.1rem;">${topic.name}</h3>
                <p style="color:#888; font-size:0.85rem; margin:0;">${topic.category}</p>
            `;

            card.addEventListener('mouseenter', () => {
                card.style.background = 'rgba(102,126,234,0.2)';
                card.style.transform = 'translateY(-3px)';
            });

            card.addEventListener('mouseleave', () => {
                card.style.background = 'rgba(102,126,234,0.1)';
                card.style.transform = 'translateY(0)';
            });

            card.addEventListener('click', () => {
                if (promptInput) promptInput.value = topic.prompt;
                modal.style.display = 'none';
                if (searchInput) searchInput.value = '';
                if (generateBtn) generateBtn.click();
            });

            listContainer.appendChild(card);
        });
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initBrowseLibrary);
} else {
    initBrowseLibrary();
}
