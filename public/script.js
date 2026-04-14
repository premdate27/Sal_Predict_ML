document.addEventListener('DOMContentLoaded', async () => {
    const form = document.getElementById('prediction-form');
    const genderSelect = document.getElementById('gender');
    const educationSelect = document.getElementById('education');
    const jobTitleSelect = document.getElementById('job_title');
    const resultContainer = document.getElementById('result-container');
    const salaryResult = document.getElementById('salary-result');
    const submitBtn = form.querySelector('button');

    // Fetch categories on load
    try {
        const response = await fetch('/api/categories');
        const categories = await response.json();

        // Populate selects
        populateSelect(genderSelect, categories.Gender);
        populateSelect(educationSelect, categories['Education Level']);
        populateSelect(jobTitleSelect, categories['Job Title']);
    } catch (err) {
        console.error("Failed to load categories:", err);
    }

    function populateSelect(selectEl, options) {
        options.forEach(opt => {
            const el = document.createElement('option');
            el.value = opt;
            el.textContent = opt;
            selectEl.appendChild(el);
        });
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Show loading state
        submitBtn.disabled = true;
        submitBtn.textContent = 'ANALYZING...';
        
        const data = {
            age: document.getElementById('age').value,
            years_exp: document.getElementById('years_exp').value,
            gender: genderSelect.value,
            education: educationSelect.value,
            job_title: jobTitleSelect.value
        };

        try {
            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            const result = await response.json();

            if (result.salary) {
                salaryResult.textContent = `$${result.salary.toLocaleString()}`;
                resultContainer.classList.remove('hidden');
                resultContainer.scrollIntoView({ behavior: 'smooth' });
            } else {
                alert("Error: " + (result.error || "Unknown error"));
            }
        } catch (err) {
            alert("Prediction failed. Make sure the API is running.");
            console.error(err);
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'PREDICT SALARY';
        }
    });
});
