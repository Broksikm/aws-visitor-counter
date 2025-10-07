// DŮLEŽITÉ: Tuto URL adresu budeme muset vyplnit po prvním nasazení!
const apiUrl = 'ZDE_BUDE_URL_Z_CLOUDFORMATION_VYSTUPU';

document.addEventListener('DOMContentLoaded', () => {
    const countElement = document.getElementById('visitor-count');

    fetch(apiUrl + '/count', { method: 'POST' })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Chyba sítě: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            countElement.textContent = data.count;
        })
        .catch(error => {
            console.error('Došlo k chybě při volání API:', error);
            countElement.textContent = 'Chyba!';
        });
});