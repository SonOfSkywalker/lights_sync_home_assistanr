import numpy as np

class ColorProcessor:
    @staticmethod
    def calculate_average_color(image, box):
        """Calculate the average color and brightness of a specific region."""
        cropped = image.crop(box)
        pixels = np.array(cropped)
        avg_color = tuple(np.mean(pixels, axis=(0, 1)).astype(int))
        brightness = int(
            np.mean(
                0.299 * pixels[..., 0] + 0.587 * pixels[..., 1] + 0.114 * pixels[..., 2]
            )
        )
        return avg_color, brightness

    @staticmethod
    def get_average_colors(image):
        """Compute average colors and brightness for 4 quadrants of a given image."""
        w, h = image.size
        quadrants = [
            (0, 0, w // 2, h // 2),
            (w // 2, 0, w, h // 2),
            (0, h // 2, w // 2, h),
            (w // 2, h // 2, w, h),
        ]
        avg_data = [ColorProcessor.calculate_average_color(image, quad) for quad in quadrants]
        avg_colors = np.array([data[0] for data in avg_data])
        avg_brightness = np.array([data[1] for data in avg_data])
        return avg_colors, avg_brightness
