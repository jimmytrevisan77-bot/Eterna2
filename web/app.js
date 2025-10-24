const modeButtons = document.querySelectorAll('.mode-switcher__btn');
const conceptSections = document.querySelectorAll('.concept');

const updateActiveConcept = (targetId) => {
  conceptSections.forEach((section) => {
    const isActive = section.id === targetId;
    section.classList.toggle('concept--active', isActive);
    section.setAttribute('aria-hidden', !isActive);
  });
};

modeButtons.forEach((button) => {
  button.addEventListener('click', () => {
    const targetId = button.dataset.target;
    updateActiveConcept(targetId);

    modeButtons.forEach((btn) => btn.classList.remove('is-active'));
    button.classList.add('is-active');
  });
});

// Accessibility: ensure the first concept is announced correctly
updateActiveConcept('concept-a');
