function toggleEdit(fieldId) {
    const field = document.getElementById(fieldId);
    console.log(`Attempting to toggle field: ${fieldId}`, field);

    if (field) {
        if (field.hasAttribute('readonly')) {
            field.removeAttribute('readonly');
            console.log(`Field ${fieldId} is now editable.`);
            field.focus();
            field.style.backgroundColor = "#ffffff";
        } else {
            field.setAttribute('readonly', true);
            console.log(`Field ${fieldId} is now readonly.`);
            field.style.backgroundColor = "#e9ecef";
        }
    } else {
        console.error(`Field with ID ${fieldId} not found.`);
    }
}


function toggleEdit(fieldId) {
    const field = document.getElementById(fieldId);
    if (field.readOnly !== undefined) {
        field.readOnly = !field.readOnly;
    }
    if (fieldId === 'bio') {
        field.focus();
        field.style.height = "auto";
        field.style.height = field.scrollHeight + "px"; // Adjust height to content
    }
}