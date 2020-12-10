$(document).ready(() => {
  const allEntriesBtn = $("#all-entries-btn");
  const newEntriesBtn = $("#new-entries-btn");

  allEntriesBtn.on('click', () => {
    window.location.href = '/allentries'
  })

  newEntriesBtn.on('click', () => {
    window.location.href = '/'
  })
})