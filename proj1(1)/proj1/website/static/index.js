function deleteCourse(courseId) {
  fetch("/delete-course", {
    method: "POST",
    body: JSON.stringify({ courseId: courseId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}
