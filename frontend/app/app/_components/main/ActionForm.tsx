import { useState, useRef, useEffect } from "react";
import { sendTalk } from "@/libs/sendTalk";
import { sendTravel } from "@/libs/sendTravel";

export interface ActionFormProps {
    mode: 'talk' | 'travel';
    sessionToken: string;
    setNpcMessage: (message: string | null) => void;
}

export default function ActionForm({ mode, sessionToken, setNpcMessage }: ActionFormProps) {
    const [inputValue, setInputValue] = useState('');
    const [loading, setLoading] = useState(false);
    const inputRef = useRef<HTMLInputElement>(null);

    useEffect(() => {
        if (!loading) {
            inputRef.current?.focus();
        }
        if (mode === 'travel') {
            setNpcMessage(null);
        }
    }, [mode, loading, setNpcMessage]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        if (mode === 'talk') {
            const { message } = await sendTalk({ sessionToken, message: inputValue });
            setNpcMessage(message);
        } else {
            await sendTravel({ sessionToken, destination: inputValue });
            setNpcMessage(null);
        }
        setInputValue('');
        setLoading(false);
    };

    const placeholder = mode === 'talk' ? "Type what you want to say..." : "Type the name of the character you want to travel to...";

    return (
        <form onSubmit={handleSubmit} className="flex-grow flex ml-4">
            <input
                ref={inputRef}
                className="bg-white opacity-90 text-gray-950 p-2 h-12 rounded-lg border-1 border-gray-800 border-solid grow"
                placeholder={placeholder}
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                disabled={loading}
            />
            <button
                type="submit" className="ml-1 bg-white text-gray-950 border-1 border-gray-800 border-solid opacity-90 rounded-lg w-12 cursor-pointer hover:opacity-100"
                disabled={loading}>
                {loading ? <i className="fa-solid fa-spinner fa-spin"></i> : <i className="fa-solid fa-check"></i>}
            </button>
        </form>
    );
}
