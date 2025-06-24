import React from "react";

const WorkFlow = () => {
  // Placeholder image; replace with your slide image path
  const slideImage = "/Space Debris WorkFlow.png";

  // Example image map coordinates and hyperlinks
  // Replace with actual coordinates and URLs from your PowerPoint slide
  const hyperlinks = [
    {
      shape: "rect",
      coords: "2280, 70, 2530, 250", // x1,y1,x2,y2 (top-left to bottom-right)
      href: "https://spacedebris.netlify.app/",
      alt: "Space Debris Website",
    },
    {
      shape: "rect",
      coords: "1725, 760,  2015, 920",
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
      coords: "1075, 425, 1360, 60",
      href: "https://dashboard.heroku.com/apps",
      alt: "Heroku PaaS",
    },
    {
      shape: "rect",
      coords: "2270, 435, 2550, 615",
      href: "https://app.netlify.com/",
      alt: "Netlify PaaS",
    },
    // Add more <area> entries as needed
  ];

  return (
    <div className="w-full h-full flex justify-center items-center bg-blue-200 p-4">
      <div className="relative max-w-full max-h-full">
        <img
          src={slideImage}
          alt="WorkFlow Slide"
          useMap="#slideMap"
          className="w-full h-auto object-contain"
        />
        <map name="slideMap">
          {hyperlinks.map((link, index) => (
            <area
              key={index}
              shape={link.shape}
              coords={link.coords}
              href={link.href}
              alt={link.alt}
              target="_blank" // Open links in new tab (optional)
              rel="noopener noreferrer" // Security for external links
            />
          ))}
        </map>
      </div>
    </div>
  );
};

export default WorkFlow;
