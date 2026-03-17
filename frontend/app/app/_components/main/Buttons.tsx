import { sendTalk } from "@/libs/sendTalk";
import { sendTravel } from "@/libs/sendTravel";

export interface ButtonsProps {
    sessionToken: string;
}

export default function Buttons({ sessionToken }: ButtonsProps) {
    const handleTalk = () => {
        // TODO: Replace with a dialog to get the message from the user
        sendTalk({ sessionToken, message: "Hello" });
    };

    const handleTravel = () => {
        // TODO: Replace with a dialog to get the destination from the user
        sendTravel({ sessionToken, destination: "the-shire" });
    };

    return (
        <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-4">
            <button
                onClick={handleTalk}
                className="flex items-center justify-center w-32 h-12 bg-white opacity-80 hover:opacity-90 text-gray-700 font-bold rounded-lg"
            >
                <i className="fa-regular fa-comment mr-2"></i>
                Talk
            </button>
            <button
                onClick={handleTravel}
                className="flex items-center justify-center w-32 h-12 bg-white opacity-80 hover:opacity-90 text-gray-700 font-bold rounded-lg"
            >
                <i className="fa-regular fa-map mr-2"></i>
                Travel
            </button>
        </div>
    );
}
