const deleteUserProfile = document.querySelector('#delete-profile');
const id = parseInt(deleteUserProfile.name);
const username = getUsernameFromId(id);
let deleted;

deleteUserProfile.addEventListener('click', function(e) {
    const deleteConfirmation = prompt("Are you sure you want to delete your user permanently? This can not be undone! Type your username here if you're sure.");
    if (deleteConfirmation === username) {
        deleted = deleteUser(id);
    };
});

async function getUsernameFromId(id) {
    resp = await axios.get(`/api/users/${id}`);
    const receivedUsername = resp.data[`${id}`].username;
    return receivedUsername;
};

async function deleteUser(id) {
    resp = await axios.delete(`/api/users/${id}`);
    const responseData = resp.data;
    return responseData;
};