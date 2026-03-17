import { useState } from "react";
import { sendTalk } from "@/libs/sendTalk";
import { sendTravel } from "@/libs/sendTravel";
import SpeechBubbleForm from "./SpeechBubbleForm";

export interface ButtonsProps {
    sessionToken: string;
}

export default function Buttons({ sessionToken }: ButtonsProps) {
    const [activeForm, setActiveForm] = useState<"talk" | "travel" | null>(null);

    const handleTalkClick = () => {
        setActiveForm(activeForm === "talk" ? null : "talk");
    };

    const handleTravelClick = () => {
        setActiveForm(activeForm === "travel" ? null : "travel");
    };

    const handleTalkConfirm = (message: string) => {
        sendTalk({ sessionToken, message });
        setActiveForm(null);
    };

    const handleTravelConfirm = (destination: string) => {
        sendTravel({ sessionToken, destination });
        setActiveForm(null);
    };

    return (
        <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-4">
            <div className="relative">
                <button
                    onClick={handleTalkClick}
                    className="flex items-center justify-center w-32 h-12 bg-white bg-opacity-20 hover:bg-opacity-30 text-white font-bold rounded-lg"
                >
                    <i className="fa-regular fa-comment mr-2"></i>
                    Talk
                </button>
                {activeForm === "talk" && (
                    <SpeechBubbleForm onConfirm={handleTalkConfirm} />
                )}
            </div>
            <div className="relative">
                <button
                    onClick={handleTravelClick}
                    className="flex items-center justify-center w-32 h-12 bg-white bg-opacity-20 hover:bg-opacity-30 text-white font-bold rounded-lg"
                >
                    <i className="fa-regular fa-map mr-2"></i>
                    Travel
                </button>
                {activeForm === "travel" && (
                    <SpeechBubbleForm onConfirm={handleTravelConfirm} />
                )}
            </div>
        </div>
    );
}
