function getPercentage(a, b) {
    return Math.round(a / b * 100)
}
// D - Fail below 36% (gray)
// C - pass between 36% and 47.99% (red)
// B - second between 48% and 54.99% (orange)
// B+ - Higher Second between 55% and 59.99% (yellow)
// A - first between 60% and 69.99% (blue)
// O - dist in between 70% and 84.99% (green)
// O+ - dist in between 85% and 100% (green)(Bold)
function getColorAccordingToMarks(marks) {
    if (marks < 36) {
        return "dark"
    } else if (marks < 48) {
        return "danger"
    } else if (marks < 55) {
        return "warning"
    } else if (marks < 60) {
        return "info"
    } else if (marks < 70) {
        return "primary"
    } else if (marks < 85) {
        return "success"
    } else {
        return "success"
    }
}