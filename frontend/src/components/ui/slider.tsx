import React from "react";

interface SliderProps extends React.InputHTMLAttributes<HTMLInputElement> {
  defaultValue?: number[];
  value?: number[];
  onValueChange?: (value: number[]) => void;
}

export const Slider: React.FC<SliderProps> = ({ className = "", defaultValue, value, onValueChange, min = 0, max = 100, step = 1, ...props }) => (
  <input
    type="range"
    className={`w-full accent-primary ${className}`}
    min={min}
    max={max}
    step={step}
    defaultValue={defaultValue?.[0]}
    value={value?.[0]}
    onChange={(e) => onValueChange?.([Number(e.target.value)])}
    {...props}
  />
);
