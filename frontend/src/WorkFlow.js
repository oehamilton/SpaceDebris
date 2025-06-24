import React, { useState, useEffect } from "react";

const WorkFlow = () => {
  // Placeholder image; ensure it's in the public folder
  const slideImage = "/Space Debris WorkFlow.png";

  // Original image dimensions (measured in MS Paint or PowerPoint export settings)
  const originalWidth = 2871; // Replace with your image's actual width
  const originalHeight = 1610; // Replace with your image's actual height

  // Initial hyperlink coordinates (from your MS Paint mapping)
  const initialHyperlinks = [
    {
      shape: "rect",
      coords: "2280, 70, 2530, 250", // x1,y1,x2,y2
      href: "https://spacedebris.netlify.app/",
      alt: "Space Debris Website",
    },
    {
      shape: "rect",
      coords: "1725, 760, 2015, 920",
      href: "https://github.com/oehamilton/SpaceDebris",
      alt: "GitHub Repository",
    },
    {
      shape: "rect",
      coords: "300, 430, 590, 600",
      href: "https://console.cloud.google.com/",
      alt: "Google Cloud",
    },
    {
      shape: "rect",
      coords: "1075, 425, 1360, 600",
      href: "https://dashboard.heroku.com/apps",
      alt: "Heroku PaaS",
    },
    {
      shape: "rect",
      coords: "2270, 435, 2550, 615",
      href: "https://app.netlify.com/",
      alt: "Netlify PaaS",
    },
  ];

  // State to hold scaled hyperlinks, image dimensions, and loading status
  const [scaledHyperlinks, setScaledHyperlinks] = useState([]);
  const [imgDimensions, setImgDimensions] = useState({ width: 0, height: 0 });
  const [isImageLoaded, setIsImageLoaded] = useState(false);

  // Handle image load and coordinate scaling
  useEffect(() => {
    const img = new Image();
    img.src = slideImage;
    img.onload = () => {
      const imgElement = document.querySelector('img[useMap="#slideMap"]');
      if (imgElement) {
        setImgDimensions({
          width: imgElement.width,
          height: imgElement.height,
        });
        const scaleX = imgElement.width / originalWidth;
        const scaleY = imgElement.height / originalHeight;
        const newHyperlinks = initialHyperlinks.map((link) => {
          const [x1, y1, x2, y2] = link.coords.split(",").map(Number);
          return {
            ...link,
            coords: `${x1 * scaleX},${y1 * scaleY},${x2 * scaleX},${
              y2 * scaleY
            }`,
          };
        });
        setScaledHyperlinks(newHyperlinks);
        setIsImageLoaded(true);
      }
    };

    // Fallback resize handler
    const handleResize = () => {
      const imgElement = document.querySelector('img[useMap="#slideMap"]');
      if (imgElement && !isImageLoaded) {
        setImgDimensions({
          width: imgElement.width,
          height: imgElement.height,
        });
        const scaleX = imgElement.width / originalWidth;
        const scaleY = imgElement.height / originalHeight;
        const newHyperlinks = initialHyperlinks.map((link) => {
          const [x1, y1, x2, y2] = link.coords.split(",").map(Number);
          return {
            ...link,
            coords: `${x1 * scaleX},${y1 * scaleY},${x2 * scaleX},${
              y2 * scaleY
            }`,
          };
        });
        setScaledHyperlinks(newHyperlinks);
        setIsImageLoaded(true);
      }
    };

    window.addEventListener("resize", handleResize);
    handleResize(); // Initial call to set coordinates

    return () => window.removeEventListener("resize", handleResize);
  }, [slideImage, originalWidth, originalHeight]);

  return (
    <div className="w-full h-full flex justify-center items-center bg-blue-200 p-4 relative">
      <div className="relative max-w-full max-h-full">
        <img
          src={slideImage}
          alt="WorkFlow Slide"
          useMap="#slideMap"
          className="w-full h-auto object-contain"
          onLoad={() => {
            const imgElement = document.querySelector(
              'img[useMap="#slideMap"]'
            );
            if (imgElement && !isImageLoaded) {
              setImgDimensions({
                width: imgElement.width,
                height: imgElement.height,
              });
              const scaleX = imgElement.width / originalWidth;
              const scaleY = imgElement.height / originalHeight;
              const newHyperlinks = initialHyperlinks.map((link) => {
                const [x1, y1, x2, y2] = link.coords.split(",").map(Number);
                return {
                  ...link,
                  coords: `${x1 * scaleX},${y1 * scaleY},${x2 * scaleX},${
                    y2 * scaleY
                  }`,
                };
              });
              setScaledHyperlinks(newHyperlinks);
              setIsImageLoaded(true);
            }
          }}
        />
        {isImageLoaded && (
          <map name="slideMap">
            {scaledHyperlinks.map((link, index) => (
              <area
                key={index}
                shape={link.shape}
                coords={link.coords}
                href={link.href}
                alt={link.alt}
                title={`${link.alt}: ${link.href}`}
                target="_blank"
                rel="noopener noreferrer"
              />
            ))}
          </map>
        )}
        {isImageLoaded &&
          scaledHyperlinks.map((link, index) => {
            const [x1, y1, x2, y2] = link.coords.split(",").map(Number);
            const width = x2 - x1;
            const height = y2 - y1;
            return (
              <div
                key={`box-${index}`}
                style={{
                  position: "absolute",
                  left: `${x1}px`,
                  top: `${y1}px`,
                  width: `${width}px`,
                  height: `${height}px`,
                  border: "2px dashed gray",
                  backgroundColor: "rgba(162, 147, 147, 0.1)",
                  pointerEvents: "none",
                  boxSizing: "border-box",
                }}
                title={link.alt}
              />
            );
          })}
      </div>
    </div>
  );
};

export default WorkFlow;
