import { useState } from "react";

export interface SpeechBubbleFormProps {
    onConfirm: (value: string) => void;
}

export default function SpeechBubbleForm({ onConfirm }: SpeechBubbleFormProps) {
    const [value, setValue] = useState("");

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onConfirm(value);
    };

    return (
        <div
            className="absolute top-0 -translate-y-full left-1/2 -translate-x-1/2 flex flex-col items-center"
        >
            <form
                onSubmit={handleSubmit}
                className="w-64 bg-white bg-opacity-90 p-4 rounded-lg"

            >
                <div className="relative">
                    <input
                        type="text"
                        value={value}
                        onChange={(e) => setValue(e.target.value)}
                        className="w-full p-2 rounded-md text-gray-800"
                        autoFocus
                    />
                    <button
                        type="submit"
                        className="absolute right-2 top-1/2 -translate-y-1/2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-1 px-2 rounded"
                    >
                        Confirm
                    </button>
                </div>
            </form>
            <div className="h-7 w-10 bg-white [clip-path:polygon(0%_0%,100%_0%,50%_100%)]"></div>
        </div>
    );
}
